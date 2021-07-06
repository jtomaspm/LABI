//os valores usados nas constantes não são reais, uma vez que a utilização de constantes com valores tão elevados seria impossível

const c = 45;
const G = 3.54;
const dt = 0.1;

let m87;

const particles = [];
let start, end;

function setup() {
  var canvas = createCanvas(windowWidth/2, windowHeight/2);
  canvas.parent('simul');
  m87 = new Blackhole(width / 2, height / 2, 10000);

  start = height / 2;
  endu = height / 2 - m87.rs * 2.6;  // valor teorico onde o fotão escaparia a força gravitica do buraco negro
  endd = height / 2 + m87.rs * 2.6;

  
}

function mousePressed(){
  if(mouseX<windowWidth/2 && mouseY<windowHeight/2 && mouseY>0 && mouseX>0){
    particles.push(new Photon(mouseX, mouseY));
  }
}




function draw() {
  background(255);

  stroke(0);
  strokeWeight(1);
  line(0, start, width, start);
  line(0, endu, width, endu);
  line(0, endd, width, endd);

  for (let p of particles) {
    m87.pull(p);
    p.update();
    p.show();
  }
  m87.show();
}