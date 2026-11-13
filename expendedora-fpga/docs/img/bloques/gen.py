INK="#1b1b1b"; Q="#5f6368"; PWR="#c62828"; SIG="#1458a8"; S5="#8e24aa"
F_IN="#e3f2fd"; F_OUT="#e8f5e9"; F_CORE="#fff3e0"; F_BRD="#f3e5f5"; F_PWR="#ffebee"; F_DBG="#eceff1"
class S:
    def __init__(s,w,h,title,sub):
        s.w,s.h=w,h; s.o=[]
        s.o.append(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' width='{w}' height='{h}' font-family='DejaVu Sans, Arial, sans-serif'>")
        s.o.append("<defs>"+"".join(f"<marker id='a{n}' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'><path d='M0,0L10,5L0,10z' fill='{c}'/></marker>" for n,c in (("i",INK),("p",PWR),("s",SIG),("v",S5)))+"</defs>")
        s.o.append(f"<rect width='{w}' height='{h}' fill='white'/>")
        s.t(30,40,title,24,w="bold"); s.t(30,64,sub,14,c=Q)
    def t(s,x,y,t,sz=13,a="start",c=INK,w="normal"):
        s.o.append(f"<text x='{x}' y='{y}' font-size='{sz}' text-anchor='{a}' fill='{c}' font-weight='{w}'>{t}</text>")
    def box(s,x,y,w,h,title,lines=(),fill=F_CORE,sz=12.5,dash=False):
        d=" stroke-dasharray='6 4'" if dash else ""
        s.o.append(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='8' fill='{fill}' stroke='{INK}' stroke-width='1.5'{d}/>")
        s.t(x+w/2,y+22,title,14,"middle",w="bold")
        for i,l in enumerate(lines): s.t(x+w/2,y+42+i*17,l,sz,"middle",Q if l.startswith("(") else INK)
    def arr(s,pts,c="i",lab=None,lx=None,ly=None,both=False,w=2):
        col={"i":INK,"p":PWR,"s":SIG,"v":S5}[c]
        st=" ".join(f"{x},{y}" for x,y in pts)
        ms=f" marker-start='url(#a{c})'" if both else ""
        s.o.append(f"<polyline points='{st}' fill='none' stroke='{col}' stroke-width='{w}' marker-end='url(#a{c})'{ms}/>")
        if lab:
            if lx is None: lx=(pts[0][0]+pts[1][0])/2; ly=(pts[0][1]+pts[1][1])/2-6
            s.t(lx,ly,lab,12,"middle",col)
    def save(s,fn):
        s.o.append("</svg>"); open(fn,"w").write("\n".join(s.o))

# ================= 1. HARDWARE =================
d=S(1600,940,"Diagrama de bloques · hardware","Máquina expendedora SED 2026-27 · qué se conecta con qué (Pmod a 3,3 V; los pines de la FPGA no toleran 5 V)")
# fuente
d.box(640,90,320,70,"Fuente 5 V · 3 A (enchufe)",["jack DC en la trasera"],F_PWR)
# placa de conexiones
d.box(560,230,480,330,"Placa de conexiones",["(primero protoboard, luego placa soldada)","reparto de 5 V y GND común (en estrella)","7 × 10 kΩ pull-up a 3,3 V (fototransistores)","7 × 220 Ω (LED IR a 5 V)","470 µF + 100 nF junto a los servos","4 × 10 kΩ pull-down (filas del numpad)","divisor de contraste del LCD","tiras de pines a JA, JB, JC, JD","conectores para desmontar cada periférico"],F_BRD)
# nexys
d.box(1150,230,400,330,"Nexys 4 DDR (sobre el techo)",["toda la lógica en VHDL","JA · barreras (7)","JB · numpad 3×4 + cancelar (8)","JC · LCD (6)","JD · servos (6)","alimentada por su jack de 5 V (JP3 en «WALL»)","USB y jack hacia atrás","7 segmentos + LED: depuración"],"#e0f7fa")
# entradas
d.box(40,180,400,150,"Rampa de monedas (pieza A)",["7 barreras IR: P1, B1-B5, P2","7 LED IR 940 nm (lado pared)","7 fototransistores (pared A-F y A-S)"],F_IN)
d.box(40,370,400,120,"Frontal: numpad 3×4 + cancelar",["producto por su número (1-4)","Cancelar: devuelve lo del escrow"],F_IN)
# salidas
d.box(40,590,400,150,"Compuertas de monedas",["SG90 #1 · trampilla del cubilete B","(retener / devolución / depósito)","SG90 #2 · trampilla del depósito C","(cerrado / hucha / devolución)"],F_OUT)
d.box(560,640,480,110,"Salida de productos",["4 × SG90 · empujador o trampilla","2 estantes × 2 productos"],F_OUT)
d.box(1150,640,400,110,"Pantalla LCD 16 × 2 (frontal)",["HD44780, modo 4 bits (RS, E, D4-D7)","RW a GND · alimentada a 5 V"],F_OUT)
d.box(1150,90,400,70,"PC (programación)",["cable USB por la trasera"],F_DBG,dash=True)
# potencia
d.arr([(800,160),(800,228)],"p","5 V",830,200)
d.arr([(1040,250),(1148,250)],"p","5 V → jack",1094,244)
d.arr([(560,260),(442,260)],"p","5 V LED",500,252)
d.arr([(560,520),(520,520),(520,620),(442,620)],"p","5 V servos",480,612)
d.arr([(800,560),(800,638)],"p","5 V servos",850,605)
d.arr([(1000,560),(1000,600),(1250,600),(1250,638)],"p","5 V LCD",1120,594)
# señales
d.arr([(442,300),(558,300)],"s","7 señales",500,292)
d.arr([(442,430),(558,430)],"s","8 señales",500,422)
d.arr([(1040,330),(1148,330)],"s","JA, JB, JC, JD",1094,322,both=True)
d.arr([(560,545),(500,545),(500,690),(442,690)],"s","2 × PWM",470,682)
d.arr([(900,560),(900,638)],"s","4 × PWM",935,605)
d.arr([(1350,560),(1350,638)],"s","RS, E, D4-D7",1405,605)
d.arr([(1350,162),(1350,228)],"i","USB",1375,200,both=True)
# leyenda
d.o.append(f"<line x1='40' y1='800' x2='80' y2='800' stroke='{PWR}' stroke-width='2.5'/>"); d.t(90,805,"alimentación 5 V",13)
d.o.append(f"<line x1='40' y1='828' x2='80' y2='828' stroke='{SIG}' stroke-width='2.5'/>"); d.t(90,833,"señal lógica 3,3 V (Pmod)",13)
d.t(40,870,"GND común a todo. Los servos aceptan la señal de 3,3 V de la FPGA. El LCD a 5 V lee bien 3,3 V (solo se le escribe, RW a GND).",13,c=Q)
d.t(40,892,"Pines: 27 de 32 usados (JA 7, JB 8, JC 6, JD 6). Quedan 5 libres para el sonido u otros extras.",13,c=Q)
d.save("bloques_hardware.svg")

# ================= 2. VHDL =================
v=S(1600,1000,"Diagrama de bloques · arquitectura VHDL","Entidad top: expendedora_top · reloj de 100 MHz de la Nexys · un testbench por módulo")
# entradas
v.box(30,120,190,90,"barreras[6:0]",["P1, B1-B5, P2 (JA)"],F_IN)
v.box(30,250,190,90,"numpad + cancelar",["3 columnas, 4 filas,","cancelar (JB)"],F_IN)
v.box(30,380,190,70,"clk 100 MHz",[],F_IN)
# etapa 1
v.box(270,110,230,110,"sincronizador",["2 biestables por señal","(evita metaestabilidad)"])
v.box(270,240,230,110,"teclado + antirrebote",["barrido del numpad 3×4","filtro 10 ms + flanco"])
v.box(270,370,230,90,"divisor_reloj",["tick_1ms, tick_1us"])
# etapa 2
v.box(560,90,280,170,"detector_monedas",["espera P1 → lee B1-B5 → P2","código termómetro → valor","5, 10, 20, 50 c, 1 € o inválida","atasco: P1 sin P2 en 2 s"])
v.box(560,290,280,120,"temporizadores",["inactividad 30 s","tiempo de giro de servos","(parámetros genéricos)"])
# núcleo
v.box(930,90,300,590,"fsm_control (Moore)",["REPOSO","MIDIENDO","ACEPTAR · RECHAZAR","SELECCION","AGOTADO (aviso)","DISPENSAR","COBRAR (depósito → hucha)","DEVOLVER (depósito → bandeja)","ATASCO","","decide posiciones de servos","y el mensaje del LCD"],F_CORE)
v.box(560,440,280,110,"credito",["saldo en céntimos","+ moneda · − precio","¿saldo ≥ precio?"])
v.box(560,580,280,140,"tabla_productos",["precios: constantes (bitstream)","stock: registro por producto,","arranca en la cantidad máxima","−1 en cada venta · agotado = 0"])
# salidas
v.box(1290,90,280,130,"pwm_servo × 6",["50 Hz, pulso 1-2 ms","2 compuertas de monedas","4 productos"],F_OUT)
v.box(1290,260,280,140,"mensajes",["textos fijos en ROM","bin → BCD del saldo y precio","«INSERTE MONEDAS», «AGOTADO»…"],F_OUT)
v.box(1290,430,280,120,"controlador_lcd",["HD44780, 4 bits","inicialización + escritura","(tiempos con tick_1us)"],F_OUT)
v.box(1290,580,280,110,"depuracion",["7 segmentos: estado y saldo","LED: barreras en vivo"],F_DBG,dash=True)
v.box(1290,760,280,80,"a los pines",["JD servos · JC LCD"],F_IN)
# flechas
v.arr([(222,165),(268,165)]); v.arr([(222,295),(268,295)]); v.arr([(222,415),(268,415)])
v.arr([(502,165),(558,165)],"s","",None,None); v.t(530,185,"sinc.",11,"middle",SIG)
v.arr([(502,278),(928,278)],"s","pulsos de botón",700,271)
v.arr([(502,415),(530,415),(530,350),(558,350)],"i","ticks",520,405)
v.arr([(842,140),(928,140)],"s","moneda_ok",885,132)
v.arr([(842,175),(928,175)],"s","valor",885,167)
v.arr([(842,210),(928,210)],"s","atasco",885,202)
v.arr([(842,340),(928,340)],"s","fin_30s",885,332)
v.arr([(842,495),(928,495)],"s","",None,None,both=True); v.t(885,487,"± saldo",11,"middle",SIG)
v.arr([(842,650),(928,650)],"s","",None,None,both=True); v.t(885,642,"precio,",11,"middle",SIG); v.t(885,672,"vender",11,"middle",SIG)
v.arr([(1232,155),(1288,155)],"s","posición",1260,147)
v.arr([(1232,330),(1288,330)],"s","",None,None); v.t(1260,322,"msg",11,"middle",SIG)
v.arr([(700,550),(700,565),(1262,565),(1262,300),(1288,300)],"s","saldo, precio (a mensajes)",1090,559)
v.arr([(1430,400),(1430,428)])
v.arr([(1232,635),(1288,635)],"s","estado",1260,627)
v.arr([(1430,220),(1430,250),(1590,250),(1590,800),(1572,800)])
v.arr([(1430,550),(1430,560),(1580,560),(1580,780),(1572,780)])
v.t(30,800,"Reset: el botón «Reset» no es el reset de la FPGA; la FSM pasa por DEVOLVER y luego vuelve a REPOSO.",13,c=Q)
v.t(30,822,"Al encender, la FSM abre el depósito hacia devolución (si se fue la luz con monedas dentro, salen).",13,c=Q)
v.t(30,844,"Precios y cantidades máximas son constantes/genéricos: cambiar un precio = cambiar una constante y regenerar el bitstream.",13,c=Q)
v.t(30,866,"Sin sensor de caída de producto (decisión 2026-11-11). Sonido: más adelante (salida de audio PWM de la Nexys).",13,c=Q)
v.save("bloques_vhdl.svg")
