import sys
import struct

from panda3d.core import Point3D, Vec3D, VBase4, CSZupRight
from panda3d.egg import EggData, EggPolygon, EggVertexPool, EggVertex

class STL2EGG():
    def __init__(self, in_file, out_file):
        #New container for data:
        self.data = EggData()

        #New Container for vertex:
        self.vertexPool = EggVertexPool('model')

        #Adding vertexPool to the main data container:
        self.data.addChild(self.vertexPool) 
        self.load(in_file)
        self.data.setCoordinateSystem(CSZupRight)
        self.data.writeEgg(out_file)

    def load(self, filename):
        f = open(filename, 'r')
        header = f.read(6)
        isASCII = ( header== 'solid ')
        if isASCII:
            self.name = f.readline()
            self.parseASCII(f)
        else:
            f.close
            f = open(filename, 'rb')
            self.parseBin(f)
                
    def getName(self):
        return self.name
           
    def readVecteur(self, data):
        v = EggVertex()
        x,y,z = struct.unpack('fff', data)        
        v.setPos(Point3D(x,y,z))
        return v 
                  
    def parseBin(self, f):
        print "Parsing Bin File"
        Header = f.read(80)
        Nb_Face = struct.unpack('i', f.read(4))[0]

        print "Nombre de face : %i" % (Nb_Face)
        for i in range(0,Nb_Face):
            self.poly = EggPolygon()
            self.data.addChild(self.poly)

            # Normal struct
            normal = self.readVecteur(f.read(12))
            u      = self.readVecteur(f.read(12))
            v      = self.readVecteur(f.read(12))
            w      = self.readVecteur(f.read(12))
            attrib   = struct.unpack('H'  , f.read(2))[0]   # Attributes

            #Adding Vertex to Triangle 
            self.poly.addVertex(self.vertexPool.addVertex(u))
            self.poly.addVertex(self.vertexPool.addVertex(v))
            self.poly.addVertex(self.vertexPool.addVertex(w))
            self.poly.recomputePolygonNormal()
            self.poly.setColor( VBase4( 0.0, 0.0, 0.5, 0.5) )

    def parseASCII(self,f ):       
        for line in f:
            line = line.lower().strip()
            commande = line.split(" ")
            Nb_Param = len(commande)
            try:
                {'facet'    : self.facet,
                 'outer'    : self.outer,
                 'vertex'   : self.vertex,
                 'endloop'  : self.endloop,
                 'endfacet' : self.endfacet}[commande[0]](commande,Nb_Param)
            except KeyError:
                pass

    def facet(self,commande,Nb_Param):
        if (Nb_Param==5 and commande[1] == "normal"):
            #We are Ignoring normal --> will be computed later
            #Creating a new polygon :
            self.poly = EggPolygon()
            self.data.addChild(self.poly)

    def outer(self,commande,Nb_Param):
        pass

    def vertex(self,commande,Nb_Param):
        if (Nb_Param==4):
            x,y,z = float(commande[1]),float(commande[2]),float(commande[3])
            if (self.poly != None):
                #Creating a new vertex with coords :
                v = EggVertex()
                v.setPos(Point3D(x,y,z))

                #Adding the new Vertex to the polygon :
                self.poly.addVertex(self.vertexPool.addVertex(v))

    def endloop(self,commande,Nb_Param):
        #End of the Loop : 
        self.poly.recomputePolygonNormal()

        #As STL files don't contain colors:
        self.poly.setColor( VBase4( 0.0, 0.0, 0.5, 0.5) )

    def endfacet(self,commande,Nb_Param):
        pass

if __name__ == "__main__":
    try:
        file_in = sys.argv[1]
        file_out = sys.argv[2]
    except:
        print "Usage : python stl2egg filename_in filename_out"
        exit()
    finally:
        app = STL2EGG(file_in, file_out)
