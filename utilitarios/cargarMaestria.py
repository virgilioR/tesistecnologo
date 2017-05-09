from controladorcamara import ControladorCamara

c = ControladorCamara()
def generarCoords(alt):
    return [{"x": -32.380289566, "y": -58.042827146, "h": alt, "tipo": 1},
            {"x": -32.38021111111111, "y": -58.04332222222222, "h": alt, "tipo": 0},
            {"x": -32.38021111111111, "y": -58.04253055555556, "h": alt, "tipo": 0},
            {"x": -32.37884722222222, "y": -58.04253055555556, "h": alt, "tipo": 0}]

c.altaRecorrido(32166,32,6,1,generarCoords(32),False,0,0,3,0,0.5,0.6)
c.altaRecorrido(32167,32,6,1,generarCoords(32),False,0,0,3,0,0.5,0.7)
#c.altaRecorrido(32168,32,6,1,generarCoords(32),False,0,0,3,0,0.5,0.8)

def generarCoords2(alt):
    return [{"x": -32.380289566, "y": -58.042827146, "h": alt, "tipo": 1},
            {"x": -32.38021111111111, "y": -58.04253055555556, "h": alt, "tipo": 0},
            {"x": -32.38021111111111, "y": -58.04173888888889, "h": alt, "tipo": 0},
            {"x": -32.37884722222222, "y": -58.04173888888889, "h": alt, "tipo": 0}]

c.altaRecorrido(32266,32,6,1,generarCoords2(32),False,0,0,3,0,0.5,0.6)
c.altaRecorrido(32267,32,6,1,generarCoords2(32),False,0,0,3,0,0.5,0.7)
#c.altaRecorrido(32268,32,6,1,generarCoords2(32),False,0,0,3,0,0.5,0.8)


"""""
def generarCoords(alt):
    return [{"x": -32.377964007, "y": -58.04322964499999, "h": alt, "tipo": 1},
            {"x": -32.37868333333333, "y": -58.04401666666667, "h": alt, "tipo": 0},
            {"x": -32.37868333333333, "y": -58.04283333333334, "h": alt, "tipo": 0},
            {"x": -32.377875, "y": -58.04283333333334, "h": alt, "tipo": 0}]

c.altaRecorrido(30466,30,6,1,generarCoords(30),False,0,0,3,0,0.5,0.6)
c.altaRecorrido(36466,36,6,1,generarCoords(36),False,0,0,3,0,0.5,0.6)
c.altaRecorrido(40466,40,6,1,generarCoords(40),False,0,0,3,0,0.5,0.6)

c.altaRecorrido(30467,30,6,1,generarCoords(30),False,0,0,3,0,0.5,0.7)
c.altaRecorrido(36467,36,6,1,generarCoords(36),False,0,0,3,0,0.5,0.7)
c.altaRecorrido(40467,40,6,1,generarCoords(40),False,0,0,3,0,0.5,0.7)

c.altaRecorrido(30468,30,6,1,generarCoords(30),False,0,0,3,0,0.5,0.8)
c.altaRecorrido(36468,36,6,1,generarCoords(36),False,0,0,3,0,0.5,0.8)
c.altaRecorrido(40468,40,6,1,generarCoords(40),False,0,0,3,0,0.5,0.8)


c.altaRecorrido(45466,45,6,1,generarCoords(40),False,0,0,3,0,0.5,0.6)
c.altaRecorrido(45467,45,6,1,generarCoords(40),False,0,0,3,0,0.5,0.7)
c.altaRecorrido(45468,45,6,1,generarCoords(40),False,0,0,3,0,0.5,0.8)
"""""
