// ===== Ascendant Effects =====
// A small home for custom ambient effects. v1: HEAT HAZE in hot biomes.
// Heat shimmer is drawn as a 2D overlay via the KubeJS Painter, so it renders OVER the world
// and OVER shaderpacks (Complementary/Oculus). Plus sparse rising heat particles.
// Logic runs server-side (PlayerEvents.tick) like the progression HUD; works in SP + MP.

const AE_JsonIO = typeof JsonIO !== "undefined" ? JsonIO : Java.loadClass("dev.latvian.mods.kubejs.util.JsonIO")

const AE_DEFAULTS = {
  heat_haze: {
    enabled: true,
    temperature_threshold: 1.5,   // base biome temp considered "hot" (desert/savanna/badlands/nether ~2.0)
    intensity: 1.0,               // overall strength multiplier
    band_count: 14,               // number of shimmer lines
    region_top: 0.46,             // shimmer region as a fraction of screen height
    region_bottom: 0.86,
    repaint_interval_ticks: 2,    // how often to re-animate (lower = smoother, higher = lighter)
    color_rgb: "FFD9A0",          // warm amber RRGGBB
    max_alpha: 30,                // cap per-line alpha (0-255); keep low = subtle
    particles_enabled: true,
    particle: "minecraft:white_ash",
    particle_chance: 0.18,
    hide_in_creative: false
  }
}

function aeIsObj(v){ return v !== null && typeof v === "object" && !Array.isArray(v) }
function aeMerge(b, o){ var r={}; Object.keys(b||{}).forEach(k=>{ r[k]=aeIsObj(b[k])?aeMerge(b[k],{}):b[k] }); Object.keys(o||{}).forEach(k=>{ r[k]=aeIsObj(o[k])&&aeIsObj(r[k])?aeMerge(r[k],o[k]):o[k] }); return r }
function aeReadConfig(){ try{ var p=AE_JsonIO.read("config/ascendant_effects/effects.json"); if(p===null||p===undefined) return AE_DEFAULTS; return aeMerge(AE_DEFAULTS,p) }catch(e){ console.warn("[Ascendant Effects] config read failed: "+e); return AE_DEFAULTS } }
let AE_cfg = aeReadConfig()

let AE_state = {}
function aeId(p){ try{ if(p&&p.uuid) return String(p.uuid) }catch(e){} return "player" }
function aeSt(p){ var id=aeId(p); if(!AE_state[id]) AE_state[id]={tick:0,wasHot:false,warned:false}; return AE_state[id] }
function aeHex2(n){ n=Math.max(0,Math.min(255,Math.floor(n))); var s=n.toString(16); return s.length<2?"0"+s:s }

const AE_HEAT_MAX_BANDS = 24
function aeClearHeat(player){ try{ var els={}; for(var i=0;i<AE_HEAT_MAX_BANDS;i++) els["ar_fx_heat_band_"+i]={remove:true}; player.paint(els) }catch(e){} }

function aeGetTemp(player){
  try{ return Number(player.block.biome.value().getBaseTemperature()) }catch(e){}
  try{ return Number(player.level.getBiome(player.blockPosition()).value().getBaseTemperature()) }catch(e){}
  return null
}
function aeBiomeId(player){ try{ return String(player.block.biomeId) }catch(e){} try{ return String(player.block.biome) }catch(e){} return "" }
const AE_HOT_WORDS = ["desert","savanna","badlands","mesa","nether","crimson","warped","basalt","soul_sand","scorch","volcan","ash","ember","sun","arid","dune","wasteland"]
function aeIsHot(player){
  var thr = Number(AE_cfg.heat_haze.temperature_threshold)
  var t = aeGetTemp(player)
  if(t !== null && !isNaN(t)) return { hot: t >= thr, temp: t }
  var id = aeBiomeId(player).toLowerCase()
  for(var i=0;i<AE_HOT_WORDS.length;i++) if(id.indexOf(AE_HOT_WORDS[i])>=0) return { hot:true, temp:2.0 }
  return { hot:false, temp:0 }
}

function aePaintHeat(player, t, hz){
  var c = AE_cfg.heat_haze
  var n = Math.max(2, Math.min(AE_HEAT_MAX_BANDS, c.band_count|0))
  var top = Number(c.region_top), bot = Number(c.region_bottom), inten = Number(c.intensity)
  var rgb = String(c.color_rgb||"FFD9A0"), maxA = Number(c.max_alpha||30)
  var els = {}
  for(var i=0;i<n;i++){
    var frac = top + (bot-top)*(i/(n-1))
    var phase = i*0.7
    var wob = Math.round(3*Math.sin(t*0.25+phase) + 2*Math.sin(t*0.13+phase*1.7))   // vertical shimmer wobble
    var groundBias = 0.40 + 0.60*((frac-top)/(bot-top))                              // stronger near the ground
    var pulse = 0.6 + 0.4*Math.sin(t*0.2+phase)
    var a = Math.round(maxA*0.55*inten*hz*groundBias*pulse)
    if(a<2)a=2; if(a>maxA)a=maxA
    els["ar_fx_heat_band_"+i] = { type:"rectangle", draw:"ingame", visible:true,
      x:"$screenW * 0", y:"$screenH * "+frac.toFixed(3)+" + ("+wob+")", z:20, w:6000, h:3, color:"#"+aeHex2(a)+rgb }
  }
  for(var j=n;j<AE_HEAT_MAX_BANDS;j++) els["ar_fx_heat_band_"+j]={remove:true}
  try{ player.paint(els) }catch(e){ var st=aeSt(player); if(!st.warned){ console.warn("[Ascendant Effects] paint failed once: "+e); st.warned=true } }
}

function aeHeatParticles(player){
  try{ player.runCommandSilent("particle "+AE_cfg.heat_haze.particle+" ~ ~0.3 ~ 5 0.4 5 0.01 3 force") }catch(e){}
}

PlayerEvents.tick(event => {
  var c = AE_cfg.heat_haze
  if(!c.enabled) return
  var player = event.player; if(!player) return
  var st = aeSt(player); st.tick++
  var interval = Math.max(1, c.repaint_interval_ticks|0)
  if(st.tick % interval !== 0) return
  if(c.hide_in_creative){ try{ if(player.isCreative()) { if(st.wasHot){ aeClearHeat(player); st.wasHot=false } return } }catch(e){} }
  var r = aeIsHot(player)
  if(r.hot){
    var hz = Math.max(0.4, Math.min(1.3, (r.temp - Number(c.temperature_threshold))*0.6 + 0.7))
    aePaintHeat(player, st.tick, hz)
    st.wasHot = true
    if(c.particles_enabled && Math.random() < Number(c.particle_chance)) aeHeatParticles(player)
  } else if(st.wasHot){
    aeClearHeat(player); st.wasHot = false
  }
})

ServerEvents.loaded(() => { AE_cfg = aeReadConfig(); console.info("[Ascendant Effects] loaded. heat_haze.enabled="+AE_cfg.heat_haze.enabled) })
