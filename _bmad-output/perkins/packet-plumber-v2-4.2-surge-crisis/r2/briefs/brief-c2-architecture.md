You are a code-review specialist reviewing ONE chunk of a larger code diff (chunk c2 of 7 — the canonical diff was 15,473 lines, split by file group per the review protocol; findings from every chunk are merged before verification). You have read-only access to the repository at the worktree path below and may verify the diff's claims against the actual codebase using read/grep/bash (read-only). NEVER modify any file, in the repo or elsewhere.

This is Perkins review ROUND 2 — a FIX-AUDIT round of PR #36 (job packet-plumber-v2-4.2-surge-crisis). Round 1 (CHANGES_REQUESTED) produced blockers B1/B2, warnings W1-W7, notes N1-N13; the diff below is the rework claiming to fix them (commit f906725, "perkins r1: stable crisis identity, frozen attribution restore, drop-site input, test-gate pins"). The round orchestrator (Perkins) runs the authoritative fix audit against the worktree. YOUR job: find NEW findings — regressions the rework introduced, new bugs, new coverage gaps, claims visibly false in your chunk. Rules:
- Do NOT re-file an r1 finding as a new finding unless the code in YOUR chunk proves a claimed fix is absent — then file it with title prefix "STILL-PRESENT: " and category "fix-audit".
- The r1 findings + claimed fixes are listed in spec/r1-findings.md; the round-2 mandate (B1/B2/W1-W7/N1-N13 verification) is spec/r2-mandate.md.

--- WORKTREE ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-4.2-surge-crisis-r2

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-4.2-surge-crisis-r2/project-context.md — it is the project's mandatory conventions (core purity, integer-only sim, determinism spine, no-globals, arena discipline, golden harness rules). Follow it when judging the diff.

--- DIFF (chunk c2) ---
diff --git a/data/crises.json b/data/crises.json
new file mode 100644
index 0000000..7dc2ad0
--- /dev/null
+++ b/data/crises.json
@@ -0,0 +1,13 @@
+{
+  "_comment": "Crisis archetype table (ODN-4/ODN-5, story 4.2) — the DATA half of the crisis engine. Each archetype names the root-cause pattern the engine evaluates (a topology flaw the player should have designed around [FORGE #3]), the failure effect, and the preventive redesign (display — what the player could have built). The SCHEDULE is NOT here: the surge set-piece lives in demand.json (the demand director consumes it — single source of truth, ODN-5); a set-piece joins an archetype via its archetype_id (fail-fast cross-ref at load). cooldown_ticks = the minimum gap between a Crisis_Resolved and a re-trigger of the same root cause (arch §6.4; 0 = re-fire allowed immediately after resolve). All sim-relevant values are integers (ODN-10); the redesign string is display content (the app renders it; determinism rides the structured refs).",
+  "archetypes": [
+    {
+      "id": "surge",
+      "display_name": "Surge",
+      "root_cause_pattern": "saturation",
+      "failure_effect": "cascade_saturation",
+      "preventive_redesign": "Add a parallel pipe or a higher tier on the spike's path.",
+      "cooldown_ticks": 0
+    }
+  ]
+}
diff --git a/data/demand.json b/data/demand.json
index 64bbc03..a304bcb 100644
--- a/data/demand.json
+++ b/data/demand.json
@@ -60,7 +60,8 @@
           "multiplier": 10,
           "start_tick": 1200,
           "duration_ticks": 1800,
-          "forecast_lead_ticks": 600
+          "forecast_lead_ticks": 600,
+          "archetype_id": "surge"
         }
       ]
     }
diff --git a/demos/surge.dem b/demos/surge.dem
new file mode 100644
index 0000000..76dabf1
--- /dev/null
+++ b/demos/surge.dem
@@ -0,0 +1,40 @@
+# surge.dem — Story 4.2's launchable golden: the surge hits on cue; you can
+# see WHY (the root cause), fix it, and watch the crisis resolve. An
+# UNPREPARED narrow-pipe path (res->router->host, 6-tile spans — narrow-
+# legal): the streaming base demand saturates the host->router bundle early
+# (service 0.167/tick — a lane at its E9 bound = dropping), so the surge
+# window opens on the flaw. At tick 1200 the surge fires (streaming x10 — the
+# director's demand multiplier); the queue is at its bound, the ladder sheds,
+# and the engine names it:
+#   Crisis_Triggered{Surge, Saturated_Bundle{bundle 1, pipe 1}} @1200
+# (golden-verified — see the T1). The player's fix lands mid-run: the flawed
+# narrows are demolished @2381 (the whole bottleneck bundle dies — the engine
+# resolves the crisis via its stable pair identity: the flaw is gone,
+# Crisis_Resolved @2381); the replacement wides land @2401, the surge's 20/tick
+# overwhelms them (2.67 service — the window is still live), the ladder sheds
+# again and the engine re-fires @2401 (dedup is per activation: a resolved
+# cause may re-trigger). The window ends @3000, base demand drains the backlog
+# below the resolve margin, and the crisis resolves for good @3000 (golden-
+# verified) — the
+# banner disappears (the 170000ms capture is the banner-gone negative proof).
+# Captures: 30000ms = the forecast countdown ("-30s") with NO banner yet;
+# 65000ms = the surge NOW + the crisis banner + the bottleneck outline;
+# 170000ms = post-resolve, the banner is gone.
+seed 4243
+run 200000ms
+era 3
+fixture off
+spawn_node residential 8 15
+spawn_node router_basic 14 15
+spawn_node content_host 20 15
+at 100ms draw 0 1 narrow
+at 100ms draw 1 2 narrow
+at 119000ms demolish pipe 0
+at 119000ms demolish pipe 1
+at 120000ms draw 0 1 wide
+at 120000ms draw 0 1 wide
+at 120000ms draw 1 2 wide
+at 120000ms draw 1 2 wide
+capture at 30000ms
+capture at 65000ms
+capture at 170000ms
diff --git a/harness/catalogs.odin b/harness/catalogs.odin
index 1cf148c..a477172 100644
--- a/harness/catalogs.odin
+++ b/harness/catalogs.odin
@@ -25,11 +25,14 @@ load_catalogs :: proc(cat: ^pp.Catalogs) -> string {
 	if e4 != nil { return fmt.tprintf("cannot read data/packet_types.json: %v", e4) }
 	dem, e5 := os.read_entire_file_from_path("data/demand.json", context.temp_allocator)
 	if e5 != nil { return fmt.tprintf("cannot read data/demand.json: %v", e5) }
+	cris, e6 := os.read_entire_file_from_path("data/crises.json", context.temp_allocator)
+	if e6 != nil { return fmt.tprintf("cannot read data/crises.json: %v", e6) }
 	src.node_types = nt
 	src.pipe_tiers = pt
 	src.balance = bal
 	src.packet_types = pkt // 3.1
 	src.demand = dem       // 3.1
+	src.crises = cris      // 4.2
 	cerr := pp.catalogs_load(cat, &src)
 	if cerr.file != "" {
 		return pp.catalog_error_string(cerr)
diff --git a/harness/goldens.odin b/harness/goldens.odin
index eaa67d7..394375d 100644
--- a/harness/goldens.odin
+++ b/harness/goldens.odin
@@ -51,6 +51,7 @@ capture_frame :: proc(rc: ^Render_Ctx, topo: ^pp.Topology, bundles: ^pp.Bundles,
 	rl.BeginDrawing()
 	rnd.draw_world(&rc.view, topo, bundles, flow, crisis, tick, {})
 	rnd.draw_forecast_panel(&rc.view, crisis, rc.view.catalogs, era)
+	rnd.draw_crisis_banner(&rc.view, crisis, rc.view.catalogs, era)
 	rl.EndDrawing()
 	img := rl.LoadImageFromScreen()
 	rl.ImageFlipVertical(&img) // framebuffer readback is bottom-up
diff --git a/goldens/boot.t1 b/goldens/boot.t1
index 026e49b..7c0236c 100644
--- a/goldens/boot.t1
+++ b/goldens/boot.t1
@@ -3,105 +3,105 @@ t1 1
 demo boot
 seed 42
 logic_hz 20
-catalog_hash bd13d5dfba445d80
+catalog_hash 8da858ab04b113db
 ticks 100
-1 f410de2b4b4e4856
-2 1b12d0458453bfd1
-3 65ea4c1cd57069b4
-4 3ce9b466d28a52cf
-5 0230b1a5a2d65a12
-6 048d11fd10b8f92d
-7 ecdfc014aa112590
-8 d996cf44c772b56b
-9 aa8dd5ad21efcb8e
-10 2044847487689de9
-11 ea8734e5d735624c
-12 4e92433975b77b67
-13 26c193b76a8353ca
-14 562737e0d6346965
-15 932582f5a0f14a28
-16 7cc994478ea295a3
-17 15274c7ffc3a2e46
-18 faaf1b1ec097c8c1
-19 c9386c85460ffa24
-20 0f0226abf01ba53f
-21 717bf9fa0bd15982
-22 4a1928bdd1583f1d
-23 add2f9c358a285c0
-24 fc69b57e573d049b
-25 1b8101b65faeb1fe
-26 30acf5f5c81dbdd9
-27 580d88e38550d73c
-28 ce506d4d1bed3957
-29 1be96d0305b1277a
-30 7fa191372ca19795
-31 c302709c1838d458
-32 f9c45ae39fe4da93
-33 3cee4d5579f0a2f6
-34 4955f8b015312f71
-35 a9cab2ab63e3e654
-36 1e2d6f96e06c786f
-37 faed760c19162a32
-38 7fe9f6daf089834d
-39 6c9f305d614554b0
-40 96b111884ce84b8b
-41 a14464eb6080b72e
-42 4b765dff2d4c1b09
-43 9db6b978ac1078ec
-44 a68743e279813b87
-45 9c264bdd11ec69ea
-46 c321d1a95cfa3905
-47 fb61d379d7c369c8
-48 0291850ae1db0943
-49 678a353d66d41666
-50 10b7e6d3d8bbf261
-51 bb114a7674f74ec4
-52 08e0b4cbfbfd4b5f
-53 f11dd3064ec9c0a2
-54 21cd8497451063bd
-55 a420e5c88a2ef360
-56 5130137d3788b73b
-57 45cd5760ef9b709e
-58 98f5a1bfcdd85379
-59 e714ddeccba7f9dc
-60 8333c69a69ddd577
-61 64fa8f6355922a9a
-62 83957b87ec530535
-63 19ca96984df091f8
-64 3363f7227bb424b3
-65 500d1ad839c2b196
-66 6d3cf910f9233711
-67 fefcf07d5f8d20f4
-68 2a42f04290f9e20f
-69 9f64ca053e491752
-70 ef982d638464676d
-71 15684a36085f60d0
-72 f9e03118ba8a4aab
-73 22af05c873a5ffce
-74 9128f4a588b31e29
-75 89555eb3fbb84d8c
-76 3d938fc8e92b0ba7
-77 079e4dee654d5a0a
-78 95ff1e21d05c65a5
-79 7c539aad12efdd68
-80 f258cfeaea6d09e3
-81 8ddb815b3ec6f386
-82 d76b89c78cdc4401
-83 ea4d4e10d3643e64
-84 398ad1fcce6e737f
-85 1b84f16e257fa7c2
-86 2fef44c1311c805d
-87 ac4b3b246a5c8800
-88 d3ef4551ed7129db
-89 7f86ec6a28b9b13e
-90 7ac52b3c5f6a9f19
-91 b4822abfe00f357c
-92 39d205b22bb2ea97
-93 49c6dc51140847ba
-94 c47c906c72e65cd5
-95 e58b7b69f9d8ca98
-96 97ac0831d1eeecd3
-97 b774150b21de6036
-98 d98933a6fe2855b1
-99 6bb1f5c2de3d6b94
-100 f849fa84485be3af
+1 2357dca94c71b428
+2 11342bfe1f0217c7
+3 43fe4bdddeb7e47e
+4 6f77502902ce99f5
+5 7c94c42c57864aac
+6 262bfadb7ba8499b
+7 7e52d777c9e79be2
+8 035a6e22e85e9669
+9 66967c62a19cff50
+10 6f509883060f480f
+11 3e02fa87c9390666
+12 8ec240e2caf686dd
+13 67732ec30b0e0874
+14 eeb0aa6b237df203
+15 08c8dbcaf8c4304a
+16 d03021cfbe62cd71
+17 91174cdb2b5ab1d8
+18 09e55789ae2f8d77
+19 70c2316d30a3af2e
+20 4f98288afaa4e825
+21 7e5864a27686735c
+22 26b440c2e9ff760b
+23 ac42d22937a98252
+24 8d84d67080279d99
+25 81451bd34ddd8580
+26 3e3087087663d0ff
+27 f27be1ebf9178f56
+28 5d89220f74782e4d
+29 d707140758f29624
+30 f76ec031b23e29b3
+31 d59ecc9d67d6143a
+32 7e0ad50a60e803e1
+33 ea4394000624ca88
+34 1386d4da55ab8f27
+35 360bc2b13dde0dde
+36 db8b2ae97d99b2d5
+37 d23637062668058c
+38 16e0837453c387fb
+39 0c03a671585b6842
+40 a2d0b1f34c4e35c9
+41 37b1670f70e51130
+42 e0bcf1b17e85946f
+43 42d72983b6b1b3c6
+44 e8e05687f875533d
+45 ed221e16ff350bd4
+46 06cd3cf8df6c0563
+47 b3c8bb529066f22a
+48 7ef6f42e51ae9751
+49 520d6bf32156ef38
+50 35b755cd4c20d7d7
+51 c89d71162d48bf0e
+52 f537a421e7277f85
+53 93398b61ca8d33bc
+54 58c2d1a7f207bf6b
+55 9bc411201b9c22b2
+56 c16017f4dc2b0679
+57 156e2138253dde60
+58 41f489f79297bd5f
+59 5f9e8d808470cab6
+60 afa9e361f2b8bfad
+61 9f216344122ef804
+62 0d6175af040bbe13
+63 c800f6fe2b1e721a
+64 43ab87e5e6534941
+65 dade160d131d8e68
+66 92d25d455476b907
+67 58260949dc392cbe
+68 baf3cbc7cb2be035
+69 487f5cb8b26393ec
+70 5f939863239ba9db
+71 82312dd949db1822
+72 6f01004cee61a9a9
+73 7ecca2b4e1de6190
+74 540e5af7a61c254f
+75 44a0871d8b5d19a6
+76 209836f96a2a161d
+77 e1e29fdc998316b4
+78 f0fc8af586f3c443
+79 fba0db9debc5058a
+80 442f03dedca907b1
+81 79a0e448a4a5ed18
+82 6470afa3069d70b7
+83 f0d4e7e6c228836e
+84 e925234ab1d41565
+85 eefbd3de006ae09c
+86 b69ac2e34a24b94b
+87 fa443e50beee9c92
+88 3ecbc240fd1c20d9
+89 b4f954b00245edc0
+90 dd48b894fe0eb13f
+91 89db85562bd88596
+92 f54ecdbbe9bdc48d
+93 adef16f3fe333164
+94 222dd942350f10f3
+95 7031315d6919247a
+96 45a4fe92d82ad721
+97 204f6263564320c8
+98 a4caba65bfce0d67
+99 f1bd3f583c58741e
+100 47017f27bf2fb115
diff --git a/goldens/bundle.t1 b/goldens/bundle.t1
index a46bf6c..8c8dd2d 100644
--- a/goldens/bundle.t1
+++ b/goldens/bundle.t1
@@ -3,75 +3,75 @@ t1 1
 demo bundle
 seed 42
 logic_hz 20
-catalog_hash bd13d5dfba445d80
+catalog_hash 8da858ab04b113db
 ticks 70
-1 332a53842c861934
-2 28faedf5135e2089
-3 34a6632db3561ebe
-4 f241bdceac674d83
-5 30ed6a513ee7d878
-6 23562dbcffee7aad
-7 1ee5f94a2b1f3922
-8 95919d2d77891af7
-9 3d2030104901109c
-10 5f8361729182d471
-11 2f62b5eed27b5fe7
-12 148e2cf90d5982e4
-13 23dbfeb0fc46f09d
-14 6a4eb903c8b02992
-15 bad827a98a98682b
-16 6b3b76bb2fb055d8
-17 a7715c896ee95e01
-18 53cbc563cddc99e6
-19 bf854f003eca466f
-20 fd557fe0cd815f4c
-21 3f69e207975b59a5
-22 f32d38d096bef85a
-23 406dbcdf8d962e33
-24 034046335b2ba720
-25 680cf1c882170689
-26 9e758e601fa59e4e
-27 d48e3aac70607df7
-28 dce5f4aec86fae74
-29 a16a27ab50b5e42d
-30 b8faad86385a07a2
-31 300602fecabe98bd
-32 0271f74adeb815dc
-33 7db5f2594a3700d3
-34 6b854a9f1e481182
-35 1ebb74242474f181
-36 12178eb87a40d230
-37 83af210e7f8a77a7
-38 67d3f3c8915ce3b6
-39 7bc91fbd162d2805
-40 51df2391c63e4024
-41 7259458c229aa69b
-42 fae4ae27b39168ca
-43 daf7fa95dd313dc9
-44 3e23fe56ab842718
-45 9afde93dda5a2f2f
-46 5ec41325d299f0be
-47 9f70c2bc7d8304ed
-48 e27e69d01955aecc
-49 86158440e9660e43
-50 1a2b81eb54acaab2
-51 a53be6eea80a476e
-52 df7687042517b321
-53 d6dacecf8e6dbf10
-54 89e5964cb30caa46
-55 f820583f6f59c7b0
-56 1a5219e0435006aa
-57 9965178d57ba7232
-58 5b59ca247f1bbbe6
-59 4bbaecf314a41495
-60 10434da18bbd96ea
-61 6d485dd03965de07
-62 aa2ccf6bed8a79fc
-63 ef351877ccecd0b9
-64 c3c368aeb643380e
-65 1535116dadad6f0b
-66 6fcd1b3db860d140
-67 cf5ff043b34a66ad
-68 34dc05e7b84aaec2
-69 028fce5b12a0197f
-70 6c7c4f43e6b44af4
+1 3c5dbcef8311982a
+2 19596758fba9700b
+3 3aa2cefdd5651c8c
+4 b6bbf21496b438c5
+5 721b0a0e3e2f1cc6
+6 73f1d47b79520e27
+7 8df956abd3561608
+8 0861fc5ee1f301f1
+9 5de8c9f90f105462
+10 17d3421c8c321743
+11 b7e4db0d7005d021
+12 6a9f2d3461e45a1a
+13 76b212e42a7b3b5f
+14 1adf0346aad14ab8
+15 9705634747d9b91d
+16 384fbf5ac5ff35f6
+17 5a655f89a685c93b
+18 04bbf0e93d766594
+19 498bd4d770bd9b99
+20 5f08e3781cfa6a52
+21 7c46a102bb830f97
+22 586346ba6b640b70
+23 0e39fa1c40903f95
+24 cf75abcaff68d80e
+25 9d2655ba5f7587f3
+26 defdf9b34aa8050c
+27 8428ced519b947b1
+28 fe78e644638cdfaa
+29 fd72ecfe56c1826f
+30 04a4842955b752c8
+31 096a14c44632b97f
+32 9ed015b1af344732
+33 8c8a568787fb5b2d
+34 272d2526561c70f8
+35 8887b46dca253e0b
+36 a7979b511683680e
+37 9af22b5d4430da29
+38 e3289ee19a5c2454
+39 1914e8c32747b8b7
+40 5ed7f39ec5ce4d0a
+41 7779432d9ef61585
+42 5faa6fa1b8ce6630
+43 c89692b01eb2aa63
+44 fe3f841de2b86226
+45 1512f2d78cd68a01
+46 b8345927e716c22c
+47 61dcce036fd203ef
+48 100d46dca0254ba2
+49 3960121a47ea615d
+50 0816a0821d398b68
+51 ddc12c765003de14
+52 72929562dfa3b75b
+53 9d4a647a39ba3316
+54 b8148b9706ed7108
+55 bdebd69c056fb3a2
+56 533e632827bc4384
+57 f49ff7b927a0ee34
+58 a11ee5ce503658c8
+59 b8144e8c8b47cf2b
+60 5af737f26025acb4
+61 e8e8f595e489515d
+62 a5cec0f16866d7ee
+63 5e885266bbae9887
+64 1c058d86bf589690
+65 feb426ca14943d09
+66 38d9db3d3048ca5a
+67 680c4bbc9eac9073
+68 e20ff2df88a034fc
+69 bc2191fb40803c85
+70 552e5c1b84b5caf6
diff --git a/goldens/demolish.t1 b/goldens/demolish.t1
index 6682b7f..22fe5f7 100644
--- a/goldens/demolish.t1
+++ b/goldens/demolish.t1
@@ -3,85 +3,85 @@ t1 1
 demo demolish
 seed 42
 logic_hz 20
-catalog_hash bd13d5dfba445d80
+catalog_hash 8da858ab04b113db
 ticks 80
-1 46b9a038363bfce2
-2 8a15b219f978e47d
-3 a27d67761052c56c
-4 4680de4e0c76c2e7
-5 64f97d7f0112a60e
-6 e19ce078d446a259
-7 52aafc34012a41b8
-8 5a1b3688742f3573
-9 de29d2c492103bba
-10 210971d55e276155
-11 c3a8c43c1253e8cc
-12 a036a92cf7a58459
-13 fad7d864643d9016
-14 9c399ef460375b53
-15 459485c39e0db808
-16 4aba808964427745
-17 75747ecc0bdc5c72
-18 70a6003f5c1acb9f
-19 14e881c6b4218bc4
-20 ff96fe8e45c69be4
-21 1b7111d83ace50ee
-22 6d2b99539a00c3c8
-23 3f7c556a8044ba9c
-24 1715f7455c03a4c1
-25 5569272670fd10a6
-26 8b2016904e544412
-27 da2d64dadea65d66
-28 e8026906402bfbc0
-29 45f2aecbc79d57bf
-30 41638c7be92b7f96
-31 d5b4b48036bef44d
-32 76447505f332c444
-33 dafa54005373be33
-34 33649c64a9a1cc4a
-35 c3c2b846afb68cd1
-36 9079c6fd6c5d2e28
-37 c3a7c6e8a24e8427
-38 6521df79d933087e
-39 b850c84d1626eab5
-40 0bbef6c7e3a9048c
-41 eba2783840aee2bb
-42 5d15f342f1c8f792
-43 ae6e8b93a08dc639
-44 32da19fc88a9ef70
-45 436441eb8637142f
-46 82d7c8c800cc9d06
-47 e589b4b77db3f9bd
-48 7cd68fac2aa77374
-49 857988bc0b5e69a3
-50 8c89bfe45ca4937a
-51 a9a0ac24138b3441
-52 d1b65bdbc43008d8
-53 d55eb354e0225c17
-54 e3216358fddd31ee
-55 8737349a99f7f525
-56 e9a22cb125f9023c
-57 68cada26cd07ab6b
-58 a467443581ff8302
-59 592435a37d48e929
-60 e79c139a0a5033a0
-61 ddd490842241249f
-62 59ab70a5382efcf6
-63 19affe09f00080ad
-64 9b887aa6b2ca60a4
-65 6ddac89e643b3c93
-66 3315c448a3083b2a
-67 238b3a4c4fe0ebb1
-68 edd9ae8de727c088
-69 809090b1a1bce987
-70 48a8e5f6cab79a5e
-71 27f5e57be8f45395
-72 b54ba0b11f67a46c
-73 7c8ee131d54cd11b
-74 80ce0365ca634672
-75 02093e67a37bf799
-76 d4b722f96da24350
-77 92e1e38c51610e8f
-78 8ddd4122e21ce166
-79 369aebdf5e49ae9d
-80 f543265d863b6d54
+1 7b90134bb0881650
+2 160d0cb80b61833f
+3 8e60532e613cb0aa
+4 246ca80ef6c6fde1
+5 e05c02753030fc24
+6 fc47351d3b2c5063
+7 24d1eb5ecd8199de
+8 361e4930498809d5
+9 5e1ac6a307430378
+10 a9c2b66a97a17027
+11 127140f7b862b652
+12 9b93d09c5dadf9cb
+13 2872c61f0f9a2c74
+14 a7807acf22b11865
+15 de968cba57be9d96
+16 e19d841a94477e2f
+17 a26208a2388da4d8
+18 6ce83cdd1cf24489
+19 45abb0e7b25854da
+20 85ca7dd24adc4612
+21 244e580c8b62755c
+22 56edb608a20c12c6
+23 f1649794686dc8aa
+24 ab2c21ecf66b625b
+25 68ebcad1c0242950
+26 43af2420c492d67c
+27 7c1e403672849868
+28 73f02820f09fe97e
+29 bb2d6857ee213c61
+30 d06eb8b719958fa4
+31 cddff69f594dd17f
+32 b9c007c05fe6b7fa
+33 8656f128ba4a4f7d
+34 8e136a364c4cfdd0
+35 f8bb4ecf5e180fab
+36 b86f5716b29f94d6
+37 df13346bfdce1f99
+38 c650d24ce0e1a7fc
+39 d161120b125c6877
+40 cf230e6329e9bb52
+41 c28b94b75884f035
+42 9dd6bdd967120228
+43 f7fb5f02adfd33c3
+44 643b137d9550b06e
+45 f3a79fc0713c6d51
+46 59fed27bdf5c8fd4
+47 686fab398670906f
+48 6529ce3d36ab3f6a
+49 ad6d781e365424ed
+50 535bed18d336e740
+51 45b6100f222f525b
+52 9a463364a81d8086
+53 a48379df441d4dc9
+54 447d195b4486b62c
+55 ec979f24c43cbda7
+56 248374e45a2d7c02
+57 5daeeb66836d9625
+58 08770c9eee2a9ed8
+59 ddff2e65123851f3
+60 6b136a2df9a80f9e
+61 3b2ede9397d2b381
+62 01865c4b518c9ec4
+63 516b28a35071ab1f
+64 f6a41e75b262f81a
+65 c4ebae8ab423619d
+66 1540c4d38183d7f0
+67 4a8c39ea46b34e4b
+68 0a53291ae9186df6
+69 2303170800cdf739
+70 26771224d04a6a1c
+71 744f82ba922c1297
+72 1f2d1527486d18f2
+73 08b1cb9e760f1255
+74 9e223061982ad6c8
+75 b80fbd20fae636e3
+76 c4bc278aebbb500e
+77 cebfa2b5f983a971
+78 5a8864dd29fc8474
+79 4ff45f700dba410f
+80 b6bffefab12cc18a
diff --git a/goldens/draw.t1 b/goldens/draw.t1
index d3e2595..5353b6c 100644
--- a/goldens/draw.t1
+++ b/goldens/draw.t1
@@ -3,65 +3,65 @@ t1 1
 demo draw
 seed 42
 logic_hz 20
-catalog_hash bd13d5dfba445d80
+catalog_hash 8da858ab04b113db
 ticks 60
-1 07782c8ccf13ffde
-2 0217ba4f427e91ed
-3 a8fd2efba17eca8c
-4 66583822a229c313
-5 f277f99a9a416f42
-6 2a7a372fa7464401
-7 9929442c18330450
-8 3c364fd9468f6457
-9 6921b98eefd9f076
-10 06cc4b21c292ee65
-11 9e2ffa97ae184e55
-12 b75c21cd030b39d0
-13 4f139b747533eddf
-14 f54ba931403cfcda
-15 ac804dfa8c6a15f9
-16 3feccbf6881f1c94
-17 6d2f841e3cadbea3
-18 dfe24b47e9c01c3e
-19 ec84cd97b035a00d
-20 0e588bbd572f2788
-21 06a4b69309cca537
-22 cc1bbc4f3f0f7772
-23 e70b527b31c7c4f1
-24 1ae76c827b50adac
-25 fdc85488861509fb
-26 524bfecb00d7efb6
-27 766bbc661ac6ab85
-28 2c18f9f1d00b4200
-29 fa6264d8a88b9c8f
-30 400d12f865cd030a
-31 f89f4be746bb55a5
-32 dc721b5364f5ce9a
-33 9a281548cbd85697
-34 3f4befb51065d3a4
-35 e837e34ec0627039
-36 9c66740018907f0e
-37 a6dcfcac3551c26b
-38 06857e459f5e20e8
-39 379e2c79d80db25d
-40 87e86cc995d0a0d2
-41 81d431756175480f
-42 caf3f7691dd4753c
-43 694d2b449781f131
-44 6f5aa04f8754e626
-45 33b40635fde7afc3
-46 d65814262fd5c500
-47 7c0973f920c164b5
-48 bfdfdc3e904c12ea
-49 85dc6d37dcdde3a7
-50 6f7fd3f314193ef4
-51 937f5a33e24d6249
-52 c79a91b58800939e
-53 fce97e19ca5a827b
-54 0a8fd1ce475b71b8
-55 d86c435f76a466ad
-56 4c5fb5b47d2478e2
-57 daa377f682eca1df
-58 776f3639c49b9e0c
-59 c91c7b5c1a6e53c1
-60 6a84271c9f0891b6
+1 4ba40d9887eaed48
+2 f8cfeab9aa71908b
+3 6667515a8eb60946
+4 f32d01f4a9a15769
+5 b5c2fe58008b9424
+6 9383c6ae5a23a7a7
+7 b532c625ca456b32
+8 bc9ff1b5cbd482e5
+9 4debaa932eeee010
+10 ccd5a7090d117e53
+11 63a90552309b5103
+12 12666b6c7765bab2
+13 c21d39643070375d
+14 b697904f58968fb4
+15 44968b1c15c16b5f
+16 ab56ed3688bf14ae
+17 99f1ae8d4682c0a9
+18 b5cfbce16d2a0860
+19 f24b5544510593eb
+20 5200f134b0ef151a
+21 c51d9638eb25c9e5
+22 41b4a12ce024819c
+23 b6ec65ac47676d47
+24 97e9662772307af6
+25 6e9664ee538db031
+26 5e42b270faca56c8
+27 d73fa4f34ff92a33
+28 9a4b713b5e047762
+29 e3cc6553c57e340d
+30 322d027eea94aa64
+31 b201fa3cf9977473
+32 da92108cb49ed874
+33 5e26c98794340975
+34 c2693236812d57c6
+35 f997e9fc918a9b1f
+36 3dc1fb7b2cb11a70
+37 5eb6b620c83fcbd1
+38 948dd3d6fedd8da2
+39 ca4ee9d26b18081b
+40 a5c68dfa8131b3fc
+41 9d0f86e0786f86dd
+42 6c48d12bff68db0e
+43 48aab355199c1307
+44 df7337ac86c08938
+45 b178034863beddb9
+46 bf05eb027adb850a
+47 e80b275a0a522403
+48 22bc124f45cd8584
+49 1d5e96d0c269ca85
+50 3c067ab5768e9616
+51 5a0c52c0fe1599ef
+52 c81ebee1222e0380
+53 21b4cadee14037a1
+54 7a6724c5b12e9eb2
+55 452ead15a87f12eb
+56 6e2da86ef8f4610c
+57 a942bdea4217e1ad
+58 80ce4f329c0b659e
+59 25607c60c2f19257
+60 fdde4f9971823f48
diff --git a/goldens/ecmp.t1 b/goldens/ecmp.t1
index 89ad50b..814405e 100644
--- a/goldens/ecmp.t1
+++ b/goldens/ecmp.t1
@@ -3,85 +3,85 @@ t1 1
 demo ecmp
 seed 42
 logic_hz 20
-catalog_hash bd13d5dfba445d80
+catalog_hash 8da858ab04b113db
 ticks 80
-1 a626f641c02ac0e2
-2 14c6ed45b9f91ed3
-3 7d4c2612f99fab78
-4 e969e681b40630e9
-5 8c808abba98b372e
-6 d66277435f86bfbf
-7 bd15c174e6119144
-8 39001be558148ad5
-9 02e1259cf56f426a
-10 cc7fdf3af232e15b
-11 43a01dcd4b8b88a2
-12 91d676a18b35bfbf
-13 7a8c0ad49286e8b8
-14 98c9f2068286d2a5
-15 cc7050f7413ac63e
-16 5f95e1b15dd5c4db
-17 2ef2a2d54ede9d44
-18 b476de48baae4391
-19 f03859f044ad822a
-20 e5c7ebbe0fb3fb65
-21 351c2b08eeb3b017
-22 04144fe3c759223a
-23 9dbcf5f3dff9085c
-24 2ebc7ee6a8c32972
-25 127940ddf30c2e01
-26 9edf77c520de9fda
-27 87fc2bbe7244e6c4
-28 83b491203b5893cc
-29 7f7be719b07143df
-30 3ef8194026d51990
-31 a3a032c6a124d08f
-32 14c58119190a9a9f
-33 92a3f4936bf572fc
-34 0f1a1f31fbe6b2c9
-35 d5d49152670a00b6
-36 0bb9dd757349414b
-37 0e81e7b376e56cc8
-38 5036f76950d10725
-39 197750fe4ae600b2
-40 97b4288dc8e62ad7
-41 6c33e44676c88574
-42 7510abf35f4473e1
-43 98287086225b642e
-44 ab027d08868a8783
-45 82ca0d587460e6c0
-46 e46d9c1e2de7df3d
-47 72d59085d80786aa
-48 6762c51ef492762f
-49 24f533a8cb7f8b0c
-50 a47c05fd4f162dd9
-51 51de01a9edd70d06
-52 420cb609040ccf1b
-53 49399ba3ff591258
-54 8c9a229cf4b1f675
-55 72ca3cbbc3c49242
-56 7e72bd61a5724767
-57 d5eae4cc197e2304
-58 69ed12ae7395c771
-59 4187ce9ddf00bdfe
-60 53d75cc810dac8d3
-61 60b5acfd6e9b8b50
-62 dee08ce3c37ed70d
-63 890cd7370bab0f3a
-64 e7d3ac1108936bbf
-65 2f1ac1d3ea66109c
-66 11180ba84433b2e9
-67 563bdee3a437f9d6
-68 bd36a7855045c56b
-69 11011d9ff650de68
-70 aaa05aded925b345
-71 041acb837715ab52
-72 4aa19185893f98f7
-73 44071a1281d18694
-74 71217a9f366c0581
-75 0cec3b59f8ae6b4e
-76 598a640f277c88a3
-77 ca94b56d5dbedf60
-78 4a78fb0448c00c5d
-79 0c8a672c6487e24a
-80 5d323795997e07cf
+1 fb700af2c9324b6c
+2 cc589a55229dde31
+3 a1dd72114c3b05fa
+4 18d3afddc0de6657
+5 839946961c82c7c0
+6 3e2e81910b6dc225
+7 33b75154312aff1e
+8 987cb313c896badb
+9 9f4b34cd69856684
+10 2f6112d71ca8e8a9
+11 b3e96eec6c062024
+12 0e74cc66e45e00ed
+13 fe8ce4cf62e7895a
+14 2b5769f792b06efb
+15 ee2af02a16dc3638
+16 93932d72ebacd9a1
+17 43b9f17aa0ce110e
+18 b302fca6c48e4eaf
+19 a280ad2ccdf0f61c
+20 bd0f6d07ad304e2b
+21 39d1e5328762316d
+22 bc94b915e55590d4
+23 a0974daa2219f5d2
+24 a0fdbd8392da3ae0
+25 371e36e4b7d9b3a3
+26 63dc5cb313803cf0
+27 bf50dd94274ba5ba
+28 ee54f5bc55133f76
+29 c3753bdd87308e45
+30 110f2c0b603766e2
+31 72bf524b5f097bed
+32 67ce6cb1864fa359
+33 6f6fb754cbd9da6a
+34 9970a92001fe7223
+35 19cbbdba5a6aab44
+36 a297c2dadb690fad
+37 01fca25b5a3c934e
+38 b707a064ab0eeb27
+39 fe275d2f745a67f8
+40 55e21abdbd4513a1
+41 1fd033d6dc8bb532
+42 e6ea24fd633c154b
+43 e735dc7a392919ec
+44 63c28c686322a3f5
+45 becc678fd4213236
+46 eee4d981ee137b4f
+47 342a528a164f9000
+48 06964c4cf3d7e429
+49 7e782fbc46bad77a
+50 49b9e362893548b3
+51 76509f30bf70b4d4
+52 d078668319cd71bd
+53 85e0a86250234dde
+54 f0af130be2b386b7
+55 229a9f66d86a7748
+56 9cadd01038394071
+57 3571cb45512bb342
+58 2dc7589ab2e8651b
+59 41eaaee83e1cd9bc
+60 741d0662a18aaa85
+61 687a1c1991571746
+62 07bfa86ccbecc61f
+63 667fa8592b5540d0
+64 967b32587a4aea39
+65 7bb1a329b36e154a
+66 4426db9c63009f03
+67 aad98ef77fde5724
+68 6092e8a39e11c80d
+69 8945764b4e65152e
+70 f572ae69db1dde07
+71 5667d4560fb519d8
+72 03357b4a92f10701
+73 f1f77dd26f53bd12
+74 6d4a450b8c2fffab
+75 5fe820c22db6054c
+76 39ecb69be2124655
+77 ed869554c17c8a96
+78 79cadda06f01072f
+79 877aae563fa340e0
+80 043b4db426a74c09
diff --git a/goldens/flow.t1 b/goldens/flow.t1
index 7e4b816..f12c9ef 100644
--- a/goldens/flow.t1
+++ b/goldens/flow.t1
@@ -3,65 +3,65 @@ t1 1
 demo flow
 seed 42
 logic_hz 20
-catalog_hash bd13d5dfba445d80
+catalog_hash 8da858ab04b113db
 ticks 60
-1 1cac863a4892477c
-2 bbc015ccb08c51eb
-3 d058b8c3d0407cbe
-4 0f58800e988e0cd5
-5 807ba5ed762eba50
-6 dd873bc42c0f339f
-7 ef004313b5ef2692
-8 ea2772daf6855f39
-9 a7ce05a897ea1724
-10 c1f26c506666b7d3
-11 13a8c4ec7b35935b
-12 8868d1760aa8ea3e
-13 ecf5f9892603dce9
-14 1c48a1d9488e6d4c
-15 e285dc80d8c0a59f
-16 0fb3b71ee55eba42
-17 128a0d5cf608ee5d
-18 adc7e6d10930e980
-19 91e2cc0753128dc3
-20 c0f1b73d6ce8ba86
-21 0c1bd83adf60be71
-22 0ad3fb214260ad34
-23 d85bdedd5293afa7
-24 b3f176344bd9edca
-25 bea9edbe5ae4a3e5
-26 3f0136f1176f09c8
-27 4ed7080cf027670b
-28 7f0ba13d272f4f6e
-29 1d332870a4e39d19
-30 a1448b888a4e917c
-31 429bfc1aeedbceb3
-32 f30b488636cc62d8
-33 7bb0c86512184ee9
-34 1b4d23c357084626
-35 3409c88f5df659b7
-36 773fff58e7ca1eac
-37 e4543a3550f4b89d
-38 2237b94e4b8cd77a
-39 133fd17485ad897b
-40 dfe008d4daf12b40
-41 cf7e9140e9f2b8bf
-42 a04943b87e1dba1b
-43 9cc2d30e3fbb290f
-44 7f0e4e2aec0fa65d
-45 b40f310314f41207
-46 5070e48d16181243
-47 8ff2beb7a54d3ea6
-48 134d50f93085fa31
-49 37a100ee438658f0
-50 db42905e6a857ae3
-51 ad1446d3920ba09a
-52 e6d4e16c98d00ca5
-53 9da869570eb7f6e4
-54 b7ecbfc1a177a407
-55 c25f16a7de3ae63e
-56 e2a2d50bf6938289
-57 42a04baea7d33a48
-58 72105d2a0f633d9b
-59 b5327fdc2f505a32
-60 e619a412d528f13d
+1 28841375d8ad839a
+2 b3e8344bda2ac85d
+3 cd2275fe6ef9ff34
+4 b15e744ced9b0eb7
+5 7a2cb97b13ba3406
+6 2dce196ce8e93549
+7 3a9e29cae4497e80
+8 df7d156ac6732053
+9 a27ffd24b9270852
+10 425e535dbae21a15
+11 0f5be0f4ffde50fd
+12 e02ec7ea33b28274
+13 6232d6a14327c913
+14 c31298dc33604ca2
+15 38601119083fd669
+16 f5d6170f25dbee30
+17 a1876e5d7867c20f
+18 278e0b1757d3c10e
+19 428dbe5191eb3615
+20 f70d8f6541339f8c
+21 232ee0d4352676ab
+22 7d92283fd578a3fa
+23 d96ea64eeda82ec1
+24 7b2add82ba186708
+25 a9a4383fa4f96ce7
+26 981f89635c1b5bc6
+27 5de57ac7fab39a2d
+28 5e17b135a4e2cea4
+29 1abb741092bb41c3
+30 5d7bfff7962ad252
+31 2075a93d34558035
+32 4243affc50572a76
+33 53c029233c1ae103
+34 080a90630d8e3f14
+35 a7abab62006b3961
+36 53fac0f3d0d7cf32
+37 d12426076feb119f
+38 8de9ea9013dc8d10
+39 f3878da23cb1144d
+40 d1413b7c173f55ce
+41 68ceeefdbdab9f3d
+42 3c5f417b6cab9599
+43 b2bfdc3e421aeded
+44 728cd83c5dc4446b
+45 272f6cd45bbcf755
+46 1d9e78f5625dc55d
+47 5b4790c56f3bacac
+48 d3f1e6337d3102d3
+49 4c54f7671b379156
+50 679d8f5cc27f311d
+51 0ed956c4689f30f8
+52 1b1ed1c951982b2f
+53 e4ba040fa74ce412
+54 0d73893b31c39c39
+55 af58a50801fc3a34
+56 146f0c1c7830e89b
+57 25de2d676cc5893e
+58 564a644a88264ea5
+59 ce5ce9cd7379c4c0
+60 24465285ede20e37
diff --git a/goldens/lose.t1 b/goldens/lose.t1
index 9b7c464..57ec1b2 100644
--- a/goldens/lose.t1
+++ b/goldens/lose.t1
@@ -3,69 +3,69 @@ t1 1
 demo lose
 seed 42
 logic_hz 20
-catalog_hash bd13d5dfba445d80
+catalog_hash 8da858ab04b113db
 ticks 64
-1 519a0a99d45b001c
-2 2fc1297202da8b1d
-3 e5cc1c6ce027ef4e
-4 224fc7359ced9347
-5 edea305cba863418
-6 51cb3e284656f099
-7 bb966b1e8b118a4a
-8 9052d0ab472ecb13
-9 53c9baaffb7500f4
-10 fd500d0198b59bf5
-11 6507a15342ec7737
-12 017e7465fda2cccc
-13 ccb92e5f76efcbd5
-14 b9a322ce233455aa
-15 c72208d534ac9853
-16 3ea32c808010a568
-17 97a774847fa3a551
-18 c708c310d8cb4186
-19 90e9c9ec6f7f16af
-20 aad0e142ee1f0664
-21 c1b9207db410a8ed
-22 dc908d3474915c22
-23 f5a6dff37c3f592b
-24 84b63924355ee640
-25 d5c7b499e152bec9
-26 97010c2a5be1befe
-27 096205879b96c247
-28 724a5b98398bd41c
-29 fd6cf7d8616dba25
-30 81d3a9e22b1f3bba
-31 46b26fc9c284bc63
-32 33ef87feb07f3df8
-33 b743a4a6adff2de1
-34 06f7f3f810caebd6
-35 5894b8f687e9937f
-36 2c33b9e1079da4f4
-37 ec413a641be8b2fd
-38 b7b383bf04307ff2
-39 788ec698a029aafb
-40 adcd69e7f6aefc50
-41 4249708c7920c526
-42 a1ea81e5879aab77
-43 6dcc6245885d901f
-44 669ad7a953bd8047
-45 8e767269ac16851f
-46 9377cc3a911e8167
-47 92f504f68dafa9ef
-48 0ef99b4d724af827
-49 e82d3fb8af7c45bf
-50 f5387a16516a4357
-51 a298c30f3252218f
-52 3fc66e453a6d1c47
-53 a1612f34691fb7ef
-54 2fa0d883a2bb9247
-55 c51c0784087d6f9f
-56 a8fcc36890f7b367
-57 3a4611b5a3d09d8f
-58 68cbc4e05c3b3317
-59 1ccca0619c008e1f
-60 0468e1500bef9a92
-61 85a8e9f832a19f28
-62 85a8e9f832a19f28
-63 85a8e9f832a19f28
-64 85a8e9f832a19f28
+1 d6d5bef6dda0ae82
+2 2b05ab0ff91316ff
+3 f2b789304825ebe4
+4 54a8fc4b6a309541
+5 2f3ec84c09c49146
+6 892f9352b53edc43
+7 62f5375f559e6de8
+8 753b708d69a67575
+9 4b3590df38badf8a
+10 6d63f29289c0cb07
+11 ff242665b69526f1
+12 5bcaa7a61aa7ebe2
+13 b46b3065b8eb1f1f
+14 66daadb4127633c8
+15 2a418b9d0df69855
+16 e8e5cdeffcf2c9d6
+17 2317eb136aa769e3
+18 26a611e4e8bb903c
+19 ba8e5bfc80d69699
+20 fe990483fe633c6a
+21 3e3301c6b62199e7
+22 799daacca57c56d0
+23 1138bd8ec4c8ed9d
+24 73364893e9f8e6be
+25 213572adb7c3a0eb
+26 9e4f62f803aefa24
+27 e4108c1852594941
+28 60138014f012caf2
+29 0ed386981f8232af
+30 f610782394c95698
+31 a55a6d8d3cdd4ee5
+32 5e6faca06c4a30a6
+33 927a9ad7daa2b8b3
+34 86e2992c1ad9a88c
+35 41182ced6af98c29
+36 a05bc7e95903aefa
+37 56c113f15e127277
+38 d697869c30d2b8a0
+39 07bd829b1a571fad
+40 491765d987e4484e
+41 78a39b96916ffb00
+42 dbed9aa0d8f2b05d
+43 3355894b2c575601
+44 d71a344545eee0f9
+45 129e081d5bc4fd35
+46 ef7792f024ea8d4d
+47 c75c0ed0c9fb27d9
+48 085c9abf677be5a1
+49 ede9d129986a06b5
+50 0345e7575dcf6ddd
+51 06c4387e75689631
+52 dc62739abf3af319
+53 cdcd8af4c9215f05
+54 ff33970a4d0e8a8d
+55 644533b8b39e43f9
+56 eeb11eed03a3d6b1
+57 c89cd4b19684bea5
+58 dee1bd75d48c303d
+59 a80f34bc85de1601
+60 68e24eb6e7683c08
+61 4176dfe58b1ee5b6
+62 4176dfe58b1ee5b6
+63 4176dfe58b1ee5b6
+64 4176dfe58b1ee5b6
diff --git a/goldens/place.t1 b/goldens/place.t1
index 5c6071b..427596a 100644
--- a/goldens/place.t1
+++ b/goldens/place.t1
@@ -3,85 +3,85 @@ t1 1
 demo place
 seed 42
 logic_hz 20
-catalog_hash bd13d5dfba445d80
+catalog_hash 8da858ab04b113db
 ticks 80
-1 49c9ddb933a984fd
-2 f1934127193541fa
-3 796bbb65e0f9aae7
-4 6f26ce2382e82d34
-5 0cb5fa2147ecda79
-6 1476a6a234dcded6
-7 d406c8d68e1f5423
-8 8ee500f46d3d0a90
-9 468389e0671e1b55
-10 1a19f888a59691f2
-11 8f115b9b77d3b6b7
-12 811e473070fd144a
-13 f54266334ca558f5
-14 a7d94989ac843748
-15 7ae0b4e67e39014b
-16 63e05d30b23a7aee
-17 c822c93c16f70c89
-18 22e2ceb177a863ec
-19 787300ce4577aeff
-20 49fee23453b61492
-21 244531949f94635d
-22 2753a2228582a0b0
-23 614cca746453fdd3
-24 74ac6ee51f011cd6
-25 cf0d6053ef0d34b1
-26 31ad0058dbd9f694
-27 9b832020b8e18ce7
-28 b7499c8d1aa53f3a
-29 2f40721559590c65
-30 f7945f2a9b25aa38
-31 89227c97fec9703b
-32 8876dc447ef7cdbc
-33 eaf5c6716e4341ad
-34 cca02da0e195b806
-35 7bc466321aeb0667
-36 9e30557d77ede9c8
-37 945d7fe74b345549
-38 763ae1d607cc4f72
-39 a2139e26e4c95a43
-40 40f3224a0ef64524
-41 ce49248cd039d535
-42 1a9077c10bf8f2ce
-43 7431bdd1f8cf8f2f
-44 83f96bc29af722b0
-45 0b720770e217ddf1
-46 0b9b0adf065e9b1a
-47 08442adce2eba2cb
-48 eb3d73a5f4549fcc
-49 550a569fd9a472fd
-50 5bf3202d944275d6
-51 f239df592581c6f7
-52 4a566eacdde3f758
-53 4b7dec1a3e0ed999
-54 c6b0a17ec7e5d102
-55 7979c6f4492b64d3
-56 04fa2c52f25a39f4
-57 b2a4e73a68ac5b45
-58 2f39b4c1bbeceb1e
-59 c41c06b64f84bcbf
-60 0362137905a5e840
-61 66bb8bc014fa3341
-62 a480514db3ba5f6a
-63 cfd998295f2862db
-64 87b899e418752d5c
-65 3b6afa20f20c29cd
-66 246440840d01c4a6
-67 3d781cbede259e07
-68 021ef0c95f1ee868
-69 814c0d02cd7c2fe9
-70 7f5e4e64e028bc92
-71 745249f61de02f63
-72 19ef63059af041c4
-73 7d504b5af0e08e55
-74 b97443212e315a6e
-75 bc28371e66cfed4f
-76 049110efd046b850
-77 df6081664663da91
-78 a8c402ed17fc34ba
-79 1da2336c1a247b6b
-80 79c265078e7f89ec
+1 ea9102995acf2c5b
+2 aa0ef4c5e4f710cc
+3 bf2ad42fb8801185
+4 98c86db23a68cb5e
+5 0acfd83e8d80971f
+6 6ad0c545ce4b7080
+7 032e2c1211dcccc9
+8 cfed9f1caed82672
+9 88c92f3da4db2fe3
+10 d5a43d09edcfe874
+11 59a2160712b3b7e9
+12 6c785c9ad68471f0
+13 46ff63b677b7038f
+14 21ab2f8e8b6ea38e
+15 3db05185d4f01a75
+16 82cc85fbfedce41c
+17 97f103e3f944397b
+18 293669c8b4b2341a
+19 d9a3ea48d13179e1
+20 f57dae8b44dad588
+21 d40fc40fde20e447
+22 9bd54b1abb3393c6
+23 1a9982ffb380e32d
+24 81c557700d9ccfd4
+25 b2b8aefc2d253713
+26 f99d8ff6f33ef1d2
+27 720007181b778799
+28 5e22a55ae96b9ae0
+29 deac5bde8e4222ff
+30 bb49783fbd71d4fe
+31 5b83da31ef67d561
+32 997a0dcdaf43f356
+33 1049efc19fb0798b
+34 6625dcb3d082b7d0
+35 e96be2675854f285
+36 12e15866e22bc20a
+37 8dd086cd2ed3654f
+38 9a7ef6cb37f000b4
+39 3cf7ddca0291a9b9
+40 2f3a2cdfe7d0d38e
+41 11aab507f47f9ac3
+42 43b99e0f90cae5c8
+43 de83b37efe25735d
+44 353d7e12b9689c82
+45 8fc95a2709db37e7
+46 d30ddcbe90f3c16c
+47 3c37949a1d2b7831
+48 d24eb18c032af6e6
+49 e659ebba0742ba1b
+50 755e010048b9d920
+51 64444c66aea8d795
+52 afc60863609f359a
+53 03f46b97cafadd9f
+54 4d9679a3cc12cc84
+55 38b41e97b6a5b1c9
+56 f2fe3c2a4492f61e
+57 bb06221e28e567d3
+58 3dd319435b147958
+59 873f763fce3bd76d
+60 f45178742648a6d2
+61 59a8b5a23e0eca37
+62 e2650c2aefc52d3c
+63 ee26fd5d977d16c1
+64 fb1391cdbdafb836
+65 d9775e8ef8e6f46b
+66 aaedb913828c6c30
+67 8ecc5ffff19283e5
+68 08ce4f348359d26a
+69 7b164814d30b422f
+70 07bb44220c546d14
+71 340276ec1d334d19
+72 fe176ff79fe5a1ee
+73 2591bc93bff7a623
+74 8b268b48f36fd5a8
+75 c524e762d482203d
+76 f1733bdaab0fce62
+77 f641f048364ff1c7
+78 614aaa1566caf2cc
+79 da1022e379d24211
+80 0c449d0c09552246
diff --git a/goldens/win.t1 b/goldens/win.t1
index 58939c3..ca9cded 100644
--- a/goldens/win.t1
+++ b/goldens/win.t1
@@ -3,65 +3,65 @@ t1 1
 demo win
 seed 42
 logic_hz 20
-catalog_hash bd13d5dfba445d80
+catalog_hash 8da858ab04b113db
 ticks 60
-1 e85e2004465de0cf
-2 de277a800bf80ff8
-3 5ae197b771a27519
-4 37b51cf23f4c655a
-5 fe30c5f861adeb63
-6 998a4733d2b1a80c
-7 ad4651a90037126d
-8 e12682e4b5a957de
-9 af8da27144c20e57
-10 b269387172896740
-11 36a44b10e4f3b522
-12 07a5c85ed6f711e7
-13 e85858cce68fe5f0
-14 dd3d767f8b505105
-15 3fdbebf47f22ad96
-16 ecb830fa7ba0987b
-17 89d6b1a4a46b9944
-18 8d6ca71c745ec6b9
-19 2656362a395311aa
-20 d88c2c9c3cf6184f
-21 7aa59c1076103138
-22 f20dda7339844fcd
-23 591ee7f4864587fe
-24 2766b47f32e447e3
-25 47a6d9f9c0aef3ac
-26 a7a67ef644520e01
-27 276bdd2344804d92
-28 b5b72598b2073a17
-29 f39ca74391298c60
-30 92f2fcc1d6c8dc35
-31 49d067c97d24649c
-32 fed0cc8a24c6694f
-33 71165d4624c86e2a
-34 96ca79b5258e4ea5
-35 5ae4664bb90a53a0
-36 2eedd95e787d2203
-37 89c7a4250e89569e
-38 760d9966d3c0f1f9
-39 630c85427e64ba64
-40 4e49a9235c100857
-41 e034a8e8e91ea798
-42 eeff697df79cd704
-43 749828e56facd974
-44 97eda458452c024e
-45 86f3981302cc3488
-46 eaac21c85613cb73
-47 93cbf5041b2784b2
-48 93cbf5041b2784b2
-49 93cbf5041b2784b2
-50 93cbf5041b2784b2
-51 93cbf5041b2784b2
-52 93cbf5041b2784b2
-53 93cbf5041b2784b2
-54 93cbf5041b2784b2
-55 93cbf5041b2784b2
-56 93cbf5041b2784b2
-57 93cbf5041b2784b2
-58 93cbf5041b2784b2
-59 93cbf5041b2784b2
-60 93cbf5041b2784b2
+1 0027769231ef2b15
+2 8d434e31aedbb002
+3 806855a9d1e97f27
+4 fc8950228f70fd84
+5 9b3fa0c2beb0e681
+6 9d72470a34608e6e
+7 4a275da9d826cf13
+8 cff3e18bd295cfc0
+9 60c60bba036ef42d
+10 6abaf04161a0729a
+11 34ce1bed3869ea64
+12 c768a73c2ad6250d
+13 768a0041aaea4d3a
+14 a01712b7c9a22adb
+15 33c2705cc8cbdf70
+16 fa73b7cb654fe529
+17 89ecf8fea85a6446
+18 b013f8c25882bd37
+19 58c7f58612bbc95c
+20 b802640b83f58345
+21 b1d1f508e0f329b2
+22 693afe9f6db61fd3
+23 70c95e49c0c52a88
+24 e3d02587e6fb6b41
+25 2a674156d8ab453e
+26 afb9fec22c28b98f
+27 c09d5c57ac1c2b14
+28 38a5763d6c57353d
+29 af2ede3378fbc5aa
+30 84e72ae141d1ebcb
+31 20c77d6c3c34f476
+32 41f1dbcd4877b635
+33 9c124f1dab67ddac
+34 c256430e476f8d2b
+35 e9dca74d3910d9e2
+36 09fc1b09ea80a271
+37 0f6cbf494a86fc68
+38 6875f6df8bfdc4e7
+39 1240beabc395ff0e
+40 b2880a72905a6b0d
+41 40e471ba77b85f0e
+42 1720ca64fe6469ca
+43 a6e365cb59cf9ada
+44 bf3ee1d451d21e7c
+45 0fc7be6d08f874e6
+46 249f9722e46bd7fd
+47 a118545cfb30ea7c
+48 a118545cfb30ea7c
+49 a118545cfb30ea7c
+50 a118545cfb30ea7c
+51 a118545cfb30ea7c
+52 a118545cfb30ea7c
+53 a118545cfb30ea7c
+54 a118545cfb30ea7c
+55 a118545cfb30ea7c
+56 a118545cfb30ea7c
+57 a118545cfb30ea7c
+58 a118545cfb30ea7c
+59 a118545cfb30ea7c
+60 a118545cfb30ea7c
diff --git a/goldens/boot.log.bin b/goldens/boot.log.bin
index 7cdfaa8..8f0942a 100644
Binary files a/goldens/boot.log.bin and b/goldens/boot.log.bin differ
diff --git a/goldens/bundle.log.bin b/goldens/bundle.log.bin
index 585ecbe..3b39e96 100644
Binary files a/goldens/bundle.log.bin and b/goldens/bundle.log.bin differ
diff --git a/goldens/demolish.log.bin b/goldens/demolish.log.bin
index 1770fd0..f0804b5 100644
Binary files a/goldens/demolish.log.bin and b/goldens/demolish.log.bin differ
diff --git a/goldens/draw.log.bin b/goldens/draw.log.bin
index b0a2f10..b4bc1c2 100644
Binary files a/goldens/draw.log.bin and b/goldens/draw.log.bin differ
diff --git a/goldens/ecmp.log.bin b/goldens/ecmp.log.bin
index b2493a8..b6dc8bc 100644
Binary files a/goldens/ecmp.log.bin and b/goldens/ecmp.log.bin differ
diff --git a/goldens/flow.log.bin b/goldens/flow.log.bin
index b0a2f10..b4bc1c2 100644
Binary files a/goldens/flow.log.bin and b/goldens/flow.log.bin differ
diff --git a/goldens/lose.log.bin b/goldens/lose.log.bin
index 975472f..241b622 100644
Binary files a/goldens/lose.log.bin and b/goldens/lose.log.bin differ
diff --git a/goldens/place.log.bin b/goldens/place.log.bin
index 078eec6..1e6917b 100644
Binary files a/goldens/place.log.bin and b/goldens/place.log.bin differ
diff --git a/goldens/win.log.bin b/goldens/win.log.bin
index b0a2f10..b4bc1c2 100644
Binary files a/goldens/win.log.bin and b/goldens/win.log.bin differ


--- SPEC / CONTEXT ---
Read ALL of these files (they are your spec; the GitHub issue is "none" — the sprint story stands in for it):
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r2/spec/job-briefing.md  (the original job briefing)
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r2/spec/story-4-2.md     (the sprint story 4.2 — the canonical acceptance criteria)
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r2/spec/gdd-crisis.md    (GDD M5 — the crisis model + fairness rules)
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r2/spec/architecture-excerpts.md (ODN-4, ODN-7, S6.4, S11.3 fairness, E10/E13)
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r2/spec/lens-guards.md   (the reviewer lens-guards — read BEFORE anything; several are BLOCKER-class)
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r2/spec/r2-mandate.md    (the round-2 fix-audit mandate)
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r2/spec/r1-findings.md   (the r1 findings + claimed fixes — the rework you are auditing)

--- YOUR LENS ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
ACCURACY MANDATE — this is the most important instruction in this brief:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

FILE-OUTPUT CONTRACT: your ONLY deliverable is the file /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r2/architecture-c2.json — write the JSON array to that exact absolute path (overwrite if it exists), then STOP. Do not write any other file. Your final message must be exactly: "DONE /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r2/architecture-c2.json <N findings>" where N is the number of findings in the array (0 is fine).