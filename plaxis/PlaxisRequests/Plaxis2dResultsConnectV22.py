
from plaxis.PlaxisRequests.Plaxis2dResultsConnectV2 import Plaxis2dResultsConnectV2



class Plaxis2dResultsConnectV22(Plaxis2dResultsConnectV2):
    def __init__(self,
                server=None, host=None, port=None, password=None
                 ):
        super(Plaxis2dResultsConnectV22, self).__init__(server, host, port, password)
    def version (self):
        return "Plaxis2dConnectV22"

    def getEmbeddedBeamResults(self,
                                  fileOut=None,
                                  tableOut=None,
                                  sphaseOrder=None,
                                  sphaseStart=None,
                                  sphaseEnd=None,
                                  ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if self.phaseOrder is None:
            print('No phases found for results')
            return -1

        print('FileOut=', fileOut)
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getEmbeddedBeamResults'
        
        # init data for lists
        ePhaseName = []
        ePhaseIdent = []
           
        eY = []
        eX = []
        
        eMat = []
        eEl = []
        
        eUx = []
        eUy = []
        eUt = []

        ePUx = []
        ePUy = []
        ePUt = []

        eU1 = []
        eU2 = []

        eM2D = []
        eQ2D = []
        eNx2D = []
        eNz2D = []

        eTskin = []
        eTlat= []

        for phase in self.phaseOrder:
            #echo ResultTypes.EmbeddedBeam
            print ('Getting EmbeddedBeam results ' + phase.Identification.value)
            try:
                embeamX = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.X, 'node')
                embeamY = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Y, 'node')
                
                embeamMat = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.MaterialID, 'node')
                embeamEl = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.ElementID, 'node')
                
                embeamUx = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Ux, 'node')
                embeamUy = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Uy, 'node')
                embeamUt = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Utot, 'node')
                
                embeamPUx = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.PUx, 'node')
                embeamPUy = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.PUy, 'node')
                embeamPUt = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.PUtot, 'node')
                 
                embeamU1 = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.U1, 'node')
                embeamU2 = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.U2, 'node')

                embeamM2D = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.M2D, 'node')
                embeamQ2D = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Q2D, 'node')
                embeamNx2D = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Nx2D, 'node')
                embeamNz2D = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Nz2D, 'node')

                embeamTskin = self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Tskin, 'node')
                embeamTlat= self.g_o.getresults(phase, self.g_o.EmbeddedBeam.Tlat, 'node')
                     
                print ('...read EmbeddedBeam results ' + phase.Identification.value)
                
                for x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat in zip(
                        embeamX, embeamY, embeamMat, embeamEl, embeamUx, embeamUy, embeamUt, embeamPUx, embeamPUy, embeamPUt, embeamU1, embeamU2, embeamM2D, embeamQ2D, embeamNx2D, embeamNz2D, embeamTskin, embeamTlat):
                    # add filters in here if necessary
                    
                    ePhaseName.append(phase.Name.value)
                    ePhaseIdent.append(phase.Identification.value)
                    eX.append(x)
                    eY.append(y)
                    eMat.append(mat)
                    eEl.append(el)
                    eUx.append(ux)
                    eUy.append(uy)
                    eUt.append(ut)
                    ePUx.append(pux)
                    ePUy.append(puy)
                    ePUt.append(put)
                    eU1.append(u1)
                    eU2.append(u2)
                    eM2D.append(m2d)
                    eQ2D.append(q2d)
                    eNx2D.append(nx2d)
                    eNz2D.append(nz2d)
                    eTskin.append(tskin)
                    eTlat.append(tlat)
            except:
                print ('...exception reading EmbeddedBeam '  + phase.Identification.value)
        columns = 'Phase,PhaseIdent,X(m),Y(m),MaterialId,ElementId,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUt(m),U1(m),U2(m),M2D(kNm/m),Q2D(kN/m),Nx2D(kN/m),Nz2D(kN/m),Tskin(kN/m),Tlat(kN/m)'
        formats = '{},{},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        if (fileOut != None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(ename, eident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat)
                                 for ename, eident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat in zip(ePhaseName, ePhaseIdent, eX, eY, eMat, eEl, eUx, eUy, eUt, ePUx, ePUy, ePUt, eU1, eU2, eM2D, eQ2D, eNx2D, eNz2D, eTskin, eTlat)])
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for ename, eident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat in zip(ePhaseName, ePhaseIdent, eX, eY, eMat, eEl, eUx, eUy, eUt, ePUx, ePUy, ePUt, eU1, eU2, eM2D, eQ2D, eNx2D, eNz2D, eTskin, eTlat):
                row = []
                row.append(ename)
                row.append(eident)
                row.append(x)
                row.append(y)
                row.append(mat)
                row.append(el)
                row.append(ux)
                row.append(uy)
                row.append(ut)
                row.append(pux)
                row.append(puy)
                row.append(put)
                row.append(u1)
                row.append(u2)
                row.append(m2d)
                row.append(q2d)
                row.append(nx2d)
                row.append(nz2d)
                row.append(tskin)
                row.append(tlat)
                
                self.insertValues(row)
                
        print('getEmbeddedBeamResults Done')