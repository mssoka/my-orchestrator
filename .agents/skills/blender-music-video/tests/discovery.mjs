// Pure installed pi skill-loader validation: no model, session, reload or settings writes.
// node discovery.mjs /absolute/pi/dist/core/skills.js /absolute/skill /absolute/future-cwd [/absolute/agent-dir]
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {pathToFileURL} from 'node:url';
const [moduleFile,skillDir,cwd,agentDir]=process.argv.slice(2);
if(!moduleFile||!skillDir||!cwd)throw Error('Supply installed pi loader, skill directory and future-job cwd');
const {loadSkills,formatSkillsForPrompt}=await import(pathToFileURL(path.resolve(moduleFile)).href);
const explicit=loadSkills({cwd:path.resolve(cwd),agentDir:agentDir||path.join(os.homedir(),'.pi','agent'),skillPaths:[path.resolve(skillDir)],includeDefaults:false});
if(explicit.skills.length!==1||explicit.diagnostics.length)throw Error(JSON.stringify(explicit));
const skill=explicit.skills[0];
if(skill.name!=='blender-music-video'||skill.disableModelInvocation)throw Error('Wrong name/trigger visibility');
const body=fs.readFileSync(skill.filePath,'utf8');
const links=[...body.matchAll(/\]\(([^)]+)\)/g)].map(m=>m[1]).filter(p=>!p.includes('://'));
for(const relative of [...links,'scripts/mv.py','scripts/native.py','scripts/recipe.py','scripts/selftest.py','tests/test_contracts.py']) {
  if(!fs.existsSync(path.resolve(skill.baseDir,relative)))throw Error('Broken skill-relative helper: '+relative);
}
const result={state:'EXPLICIT_PI_DISCOVERY_PASSED',name:skill.name,baseDir:skill.baseDir,cwd:path.resolve(cwd),diagnostics:explicit.diagnostics,relativeLinks:links,promptVisible:formatSkillsForPrompt(explicit.skills).includes('blender-music-video'),modelOrSessionStarted:false};
if(agentDir){
  const defaults=loadSkills({cwd:path.resolve(cwd),agentDir:path.resolve(agentDir),skillPaths:[],includeDefaults:true});
  const matches=defaults.skills.filter(s=>s.name===skill.name);
  const collisions=defaults.diagnostics.filter(d=>JSON.stringify(d).includes(skill.name));
  if(matches.length!==1||collisions.length||fs.realpathSync(matches[0].filePath)!==fs.realpathSync(skill.filePath))throw Error(JSON.stringify({matches,collisions}));
  result.defaultDiscovery='PASSED';result.globalMatch=matches[0].filePath;result.unrelatedDiagnosticCount=defaults.diagnostics.length;
}
console.log(JSON.stringify(result,null,2));
