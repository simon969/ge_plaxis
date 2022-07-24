from plaxis.PlaxisRequests.PlaxisResults import Plaxis2dResults

class Plaxis2dResults2019 (Plaxis2dResults):
    def __init__(self,
                server=None, host=None, port=None, password=None
                 ):
        super(Plaxis2dResults2019, self).__init__(server, host, port, password)
    def version (self):
        return "Plaxis2d2019"

    def getPlateResults(self,
                        fileOut=None,
                        tableOut=None,
                        sphaseOrder=None,
                        sphaseStart=None,
                        sphaseEnd=None
                        ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if self.phaseOrder is None:
            print('No phases found for results')
            return -1

        print('FileOut=', fileOut)
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getPlateResults'
        
        # init data for lists
        pPhaseName = []
        pPhaseIdent = []
           
        pY = []
        pX = []
        
        pMat = []
        pEl = []
         
        pUx = []
        pUy = []
        pUt = []

        pPUx = []
        pPUy = []
        pPUt = []

        pU1 = []
        pU2 = []

        pM2D = []
        pQ2D = []
        pNx2D = []
        pNz2D = []



        for phase in self.phaseOrder:
            print('Getting Plate results ' + phase.Identification.value)
            
            try: 
                plateX = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.X, 'node')
                plateY = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Y, 'node')
                
                plateMat = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.MaterialID, 'node')
                plateEl = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.ElementID, 'node')      
                
                plateUx = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Ux, 'node')
                plateUy = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Uy, 'node')
                plateUt = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Utot, 'node')

                platePUx = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUx, 'node')
                platePUy = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUy, 'node')
                platePUt = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.PUtot, 'node')

                plateU1 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.U1, 'node')
                plateU2 = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.U2, 'node')

                plateM2D = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.M2D, 'node')
                plateQ2D = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Q2D, 'node')
                plateNx2D = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Nx2D, 'node')
                plateNz2D = self.g_o.getresults(phase, self.g_o.ResultTypes.Plate.Nz2D, 'node')
                
                print('...read Plate results ' + phase.Identification.value)
                
                for x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d in zip(
                        plateX, plateY, plateMat, plateEl, plateUx, plateUy, plateUt, platePUx, platePUy, platePUt, plateU1, plateU2, plateM2D, plateQ2D, plateNx2D, plateNz2D):
                    # add filters in here if necessary
                    pPhaseName.append(phase.Name.value)
                    pPhaseIdent.append(phase.Identification.value)
                    pX.append(x)
                    pY.append(y)
                    pMat.append(mat)
                    pEl.append(el)
                    pUx.append(ux)
                    pUy.append(uy)
                    pUt.append(ut)
                    pPUx.append(pux)
                    pPUy.append(puy)
                    pPUt.append(put)
                    pU1.append(u1)
                    pU2.append(u2)
                    pM2D.append(m2d)
                    pQ2D.append(q2d)
                    pNx2D.append(nx2d)
                    pNz2D.append(nz2d)
                    
            except Exception as e:
                print ('...exception reading Plate results ' + phase.Identification.value + str(e))
                self.logger.error('...exception reading Plate results  '+ str(e))
                
        columns ='Phase,PhaseIdent,X(m),Y(m),MaterialID,ElementID,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUt(m),U1(m),U2(m),M2D(kNm/m),Q2D(kN/m),Nx2D(kN/m),Nz2D(kN/m)'
        formats = '{},{},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        if (fileOut == None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to string....')
            rows = ''.join([formats.format(pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d)
            for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d in zip(pPhaseName, pPhaseIdent, pX, pY, pMat, pEl, pUx, pUy, pUt, pPUx, pPUy, pPUt, pU1, pU2, pM2D, pQ2D, pNx2D, pNz2D)])
            return columns + rows

        if (fileOut != None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines(columns)
                file.writelines([formats.format(pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d)
                                 for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d in zip(pPhaseName, pPhaseIdent, pX, pY, pMat, pEl, pUx, pUy, pUt, pPUx, pPUy, pPUt, pU1, pU2, pM2D, pQ2D, pNx2D, pNz2D)])
            return "Plate results written to file:" + fileOut 
        
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d in zip(pPhaseName, pPhaseIdent, pX, pY, pMat, pEl, pUx, pUy, pUt, pPUx, pPUy, pPUt, pU1, pU2, pM2D, pQ2D, pNx2D, pNz2D):
                row = []
                row.append(pname)
                row.append(pident)
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
                
                self.insertValues(row)
            return "Plate results written to file:" + fileOut + " table:" + tableOut    
        print('getPlateResults Done')
       
        
    def getEmbeddedBeamRowResults(self,
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
            tableOut = 'getEmbeddedBeamRowResults'
        
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
            #echo ResultTypes.EmbeddedBeamRow
            print ('Getting EmbeddedBeamRow results ' + phase.Identification.value)
            try:
                embeamX = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeamRow.X, 'node')
                embeamY = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeamRow.Y, 'node')
                
                embeamMat = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeamRow.MaterialID, 'node')
                embeamEl = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeamRow.ElementID, 'node')
                
                embeamUx = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeamRow.Ux, 'node')
                embeamUy = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeamRow.Uy, 'node')
                embeamUt = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeamRow.Utot, 'node')
                
                embeamPUx = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeamRow.PUx, 'node')
                embeamPUy = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeamRow.PUy, 'node')
                embeamPUt = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeamRow.PUtot, 'node')
                 
                embeamU1 = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeamRow.U1, 'node')
                embeamU2 = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeamRow.U2, 'node')

                embeamM2D = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeamRow.M2D, 'node')
                embeamQ2D = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeamRow.Q2D, 'node')
                embeamNx2D = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeamRow.Nx2D, 'node')
                embeamNz2D = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeamRow.Nz2D, 'node')

                embeamTskin = self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeamRow.Tskin, 'node')
                embeamTlat= self.g_o.getresults(phase, self.g_o.ResultTypes.EmbeddedBeamRow.Tlat, 'node')
                     
                print ('...read EmbeddedBeamRow results ' + phase.Identification.value)
                
                for x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat in zip(
                        embeamX, embeamY, embeamMat, embeamUx, embeamUy, embeamUt, embeamPUx, embeamPUy, embeamPUt, embeamU1, embeamU2, embeamM2D, embeamQ2D, embeamNx2D, embeamNz2D, embeamTskin, embeamTlat):
                    # add filters in here if necessary
                    
                    ePhaseName.append(phase.Name.value)
                    ePhaseIdent.append(phase.Identification.value)
                    eX.append(x)
                    eY.append(y)
                    eMat.append(mat)
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
            except Exception as e:
                print ('...exception reading EmbeddedBeamRow results ' + phase.Identification.value + str(e))
                self.logger.error('...exception reading EmbeddedBeamRow results  '+ str(e))
        columns = 'Phase,PhaseIdent,X(m),Y(m),MaterialId,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUt(m),U1(m),U2(m),M2D(kNm/m),Q2D(kN/m),Nx2D(kN/m),Nz2D(kN/m),Tskin(kN/m),Tlat(kN/m)'
        formats = '{},{},{:2f},{:2f},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        if (fileOut == None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to string....')
            rows = ''.join([formats.format(ename, eident, x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat)
                                 for ename, eident, x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat in zip(ePhaseName, ePhaseIdent, eX, eY, eMat, eUx, eUy, eUt, ePUx, ePUy, ePUt, eU1, eU2, eM2D, eQ2D, eNx2D, eNz2D, eTskin, eTlat)])
            return columns + rows
        
        if (fileOut != None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(ename, eident, x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat)
                                 for ename, eident, x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat in zip(ePhaseName, ePhaseIdent, eX, eY, eMat, eUx, eUy, eUt, ePUx, ePUy, ePUt, eU1, eU2, eM2D, eQ2D, eNx2D, eNz2D, eTskin, eTlat)])
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for ename, eident, x, y, mat, ux, uy, ut, pux, puy, put, u1, u2, m2d, q2d, nx2d, nz2d, tskin, tlat in zip(ePhaseName, ePhaseIdent, eX, eY, eMat, eUx, eUy, eUt, ePUx, ePUy, ePUt, eU1, eU2, eM2D, eQ2D, eNx2D, eNz2D, eTskin, eTlat):
                row = []
                row.append(ename)
                row.append(eident)
                row.append(x)
                row.append(y)
                row.append(mat)
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
    def getNodeToNodeAnchorResults(self,
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
            tableOut = 'getNodeToNodeAnchorResults'
            
        # init data for lists
        aPhaseName = []
        aPhaseIdent = []
        
        aY = []
        aX = []
        
        aMat = []
        aEl = []
        
        aUx = []
        aUy = []
        
        aPUx = []
        aPUy = []
        aPUt = []
        aUt = []
        aU1 = []
        aU2 = []
        
        aForce2D = []

        for phase in self.phaseOrder:

            print('Getting NodeToNodeAnchor results for Phase ', phase.Name.value, phase.Identification.value)
            try:
                anchorX = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.X, 'node')
                anchorY = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.Y, 'node')
                
                anchorMat = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.MaterialID, 'node')
                anchorEl = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.ElementID, 'node')
                
                anchorUx = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.Ux, 'node')
                anchorUy = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.Uy, 'node')
                anchorUt = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.Utot, 'node')

                anchorPUx = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.PUx, 'node')
                anchorPUy = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.PUy, 'node')
                anchorPUt = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.PUtot, 'node')

                anchorU1 = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.U1, 'node')
                anchorU2 = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.U2, 'node')

                anchorForce2D = self.g_o.getresults(phase, self.g_o.ResultTypes.NodeToNodeAnchor.AnchorForce2D, 'node')

                for x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, f2D in zip(
                        anchorX, anchorY, anchorMat, anchorEl, anchorUx, anchorUy, anchorUt, anchorPUx, anchorPUy, anchorPUt, anchorU1, anchorU2, anchorForce2D):
                    # add filters in here if necessary
                    aPhaseName.append(phase.Name.value)
                    aPhaseIdent.append(phase.Identification.value)
                    aX.append(x)
                    aY.append(y)
                    aMat.append(mat)
                    aEl.append(el)
                    aUx.append(ux)
                    aUy.append(uy)
                    aUt.append(ut)
                    aPUx.append(pux)
                    aPUy.append(puy)
                    aPUt.append(put)
                    aU1.append(u1)
                    aU2.append(u2)
                    aForce2D.append(f2D)
            except Exception as e:
                print ('...exception reading NodeToNodeAnchor results ' + phase.Identification.value + str(e))
                self.logger.error('...exception reading NodeToNodeAnchor results  '+ str(e))
        columns = 'Phase,PhaseIdent,X(m),Y(m),MaterialId,ElementId,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUtot(m),U1(m),U2(m),N(kN)'
        formats = '{},{},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        if (fileOut == None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to string....')
            rows = ''.join([formats.format(pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, f2d)
                                 for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, f2d in zip(aPhaseName, aPhaseIdent, aX, aY, aMat, aEl, aUx, aUy, aUt, aPUx, aPUy, aPUt, aU1, aU2, aForce2D)])
            return columns + rows
        
        if (fileOut != None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, f2d)
                                 for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, f2d in zip(aPhaseName, aPhaseIdent, aX, aY, aMat, aEl, aUx, aUy, aUt, aPUx, aPUy, aPUt, aU1, aU2, aForce2D)])
        
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, f2d in zip(aPhaseName, aPhaseIdent, aX, aY, aMat, aEl, aUx, aUy, aUt, aPUx, aPUy, aPUt, aU1, aU2, aForce2D):
                row = []
                row.append(pname)
                row.append(pident)
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
                row.append(f2d)
                
                self.insertValues(row)
                
        print('getNodeToNodeAnchorResults Done')
   
    def getFixedEndAnchorResults(self,
                                 fileOut=None,
                                 tableOut=None,
                                 sphaseOrder=None,
                                 sphaseStart=None,
                                 sphaseEnd=None
                                 ):

        self.setPhaseOrder(sphaseOrder,
                           sphaseStart,
                           sphaseEnd)

        if self.phaseOrder is None:
            print('No phases found for results')
            return -1

        print('FileOut=', fileOut)
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getFixedEndAnchorResults'
        
        # init data for lists
        aPhaseName = []
        aPhaseIdent = []

        aY = []
        aX = []
        
        aMat = []
        aEl = []
        
        aUx = []
        aUy = []
        aPUx = []
        aPUy = []
        aPUt = []
        aUt = []
        aU1 = []
        aU2 = []
        
        aForce2D = []

        for phase in self.phaseOrder:

            print('Getting FixedEndAnchor results for ', phase.Name.value)
            try:
                anchorX = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.X, 'node')
                anchorY = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.Y, 'node')
                
                anchorMat = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.MaterialID, 'node')
                anchorEl = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.ElementID, 'node')
                
                anchorUx = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.Ux, 'node')
                anchorUy = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.Uy, 'node')
                anchorUt = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.Utot, 'node')

                anchorPUx = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.PUx, 'node')
                anchorPUy = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.PUy, 'node')
                anchorPUt = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.PUtot, 'node')

                anchorU1 = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.U1, 'node')
                anchorU2 = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.U2, 'node')

                anchorForce2D = self.g_o.getresults(phase, self.g_o.ResultTypes.FixedEndAnchor.AnchorForce2D, 'node')
                
                print('Retrieved FixedEndAnchor results for ', phase.Name.value)
          
                for x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, f2D in zip(
                        anchorX, anchorY, anchorMat, anchorEl, anchorUx, anchorUy, anchorUt, anchorPUx, anchorPUy, anchorPUt, anchorU1, anchorU2, anchorForce2D):
                    # add filters in here if necessary
                    aPhaseName.append(phase.Name.value)
                    aPhaseIdent.append(phase.Identification.value)
                    aX.append(x)
                    aY.append(y)
                    aMat.append(mat)
                    aEl.append(el)
                    aUx.append(ux)
                    aUy.append(uy)
                    aUt.append(ut)
                    aPUx.append(pux)
                    aPUy.append(puy)
                    aPUt.append(put)
                    aU1.append(u1)
                    aU2.append(u2)
                    aForce2D.append(f2D)
            except Exception as e:
                print ('...exception reading FixedEndAnchor results ' + phase.Identification.value + str(e))
                self.logger.error('...exception reading FixedEndAnchor results  '+ str(e))
        columns = 'Phase,PhaseIdent,X(m),Y(m),MaterialId,ElementId,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUtot(m),U1(m),U2(m),N(kN)'
        formats = '{},{},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        if (fileOut == None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to string....')
            rows = ''.join([formats.format(pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, f2d)
                                 for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, f2d in zip(aPhaseName, aPhaseIdent, aX, aY, aMat, aEl, aUx, aUy, aUt, aPUx, aPUy, aPUt, aU1, aU2, aForce2D)])
            return columns + rows
        
        if (fileOut != None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, f2d)
                                 for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, f2d in zip(aPhaseName, aPhaseIdent, aX, aY, aMat, aEl, aUx, aUy, aUt, aPUx, aPUy, aPUt, aU1, aU2, aForce2D)])
        
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, f2d in zip(aPhaseName, aPhaseIdent, aX, aY, aMat, aEl, aUx, aUy, aUt, aPUx, aPUy, aPUt, aU1, aU2, aForce2D):
                 row = []
                 row.append(pname)
                 row.append(pident)
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
                 row.append(f2d)
                 
                 self.insertValues(row)
                 
        print('getFixedEndAnchorResults Done')
    def getInterfaceResults(self,
                    fileOut=None,
                    tableOut=None,
                    sphaseOrder=None,
                    sphaseStart=None,
                    sphaseEnd=None
                    ):
        self.setPhaseOrder(sphaseOrder,
           sphaseStart,
           sphaseEnd)
        if self.phaseOrder is None:
            print('No phases found for results')
            return -1

        print('FileOut=', fileOut)
        
        if (self.IsDbFile(fileOut) and not tableOut):
            tableOut = 'getInterfaceResults'
        
        # init data for lists
        iPhaseName = []
        iPhaseIdent = []

        iY = []
        iX = []
        iMat = []
        iEl = []
        
        iUx = []
        iUy = []
        iUt = []

        iPUx = []
        iPUy = []
        iPUt = []

        iU1 = []
        iU2 = []

        iEffNormalStress = []
        iTotNormalStress = []
        iShearStress = []
        iRelShearStress = []

        iPExcess = []
        iPActive = []
        iPSteady = []
        iPWater = []
        
        iSuction = []
        iEffSuction = []

        for phase in self.phaseOrder:

            print('Getting Interface results for Phase ', phase.Name.value)
            try:
                interX = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.X, 'node')
                interY = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Y, 'node')
              
                interMat = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.MaterialID, 'node')
                interEl = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.ElementID, 'node')
              
                interUx = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Ux, 'node')
                interUy = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Uy, 'node')
                interUt = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Utot, 'node')

                interPUx = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PUx, 'node')
                interPUy = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PUy, 'node')
                interPUt = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PUtot, 'node')

                interU1 = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.U1, 'node')
                interU2 = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.U2, 'node')

                interEffNormalStress = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.InterfaceEffectiveNormalStress, 'node')
                interTotNormalStress = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.InterfaceTotalNormalStress, 'node')
                interShearStress = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.InterfaceShearStress, 'node')
                interRelShearStress = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.InterfaceRelativeShearStress, 'node')

                interPExcess = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PExcess, 'node')
                interPActive = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PActive, 'node')
                interPSteady = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PSteady, 'node')
                interPWater = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.PWater, 'node')
                
                interSuction = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.Suction, 'node')
                interEffSuction = self.g_o.getresults(phase, self.g_o.ResultTypes.Interface.EffSuction, 'node')

                for x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, ens, tns, ss, rss, pe, pa, pst, pw, su, esu in zip(
                        interX, interY, interMat, interEl, 
                        interUx, interUy, interUt, 
                        interPUx, interPUy, interPUt, 
                        interU1, interU2, 
                        interEffNormalStress, interTotNormalStress, interShearStress, interRelShearStress,
                        interPExcess, interPActive, interPSteady, interPWater, 
                        interSuction,  interEffSuction):
                    # add filters in here if necessary
                    iPhaseName.append(phase.Name.value)
                    iPhaseIdent.append(phase.Identification.value)
                    iX.append(x)
                    iY.append(y)
                    iMat.append(mat)
                    iEl.append(el)
                    iUx.append(ux)
                    iUy.append(uy)
                    iUt.append(ut)
                    iPUx.append(pux)
                    iPUy.append(puy)
                    iPUt.append(put)
                    iU1.append(u1)
                    iU2.append(u2)
                    iEffNormalStress.append(ens)
                    iTotNormalStress.append(tns)
                    iShearStress.append(ss)
                    iRelShearStress.append(rss)
                    iPExcess.append(pe)
                    iPActive.append(pa)
                    iPSteady.append(pst)
                    iPWater.append(pw)
                    iSuction.append(su)
                    iEffSuction.append(esu)
            except Exception as e:
                print ('...exception reading Interface results ' + phase.Identification.value + str(e))
                self.logger.error('...exception reading Interface results  '+ str(e))
        
        columns = "Phase,PhaseIdent,X(m),Y(m),MaterialId,ElementId,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUt(m),U1(m),U2(m),Eff NormalStress (kPa),Tot Normal Stress (kPa),Shear Stress (kPa),Rel Shear Stress (kPa),Excess Porewater (kPa),Active Porewater (kPa),Steady Porewater (kPa),Suction Porewater (kPa),Porewater (kPa),Effective Suction Porewater (kPa)"
        formats = "{},{},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}"
        
        if (fileOut == None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to string....')
            rows = ''.join([formats.format(pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, ens, tns, ss, rss, pe, pa, pst, pw, su, esu)
                                 for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, ens, tns, ss, rss, pe, pa, pst, pw, su, esu 
                                 in zip(iPhaseName, iPhaseIdent, iX, iY, iMat, iEl, iUx, iUy, iUt, iPUx, iPUy, iPUt, iU1, iU2, iEffNormalStress, iTotNormalStress, iShearStress, iRelShearStress, iPExcess, iPActive, iPSteady, iPWater, iSuction, iEffSuction)])
            return columns + rows

        if (fileOut != None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to file ', fileOut, '....')
            with open(fileOut, "w") as file:
                file.writelines([columns])
                file.writelines([formats.format(pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, ens, tns, ss, rss, pe, pa, pst, pw, su, esu)
                                 for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, ens, tns, ss, rss, pe, pa, pst, pw, su, esu 
                                 in zip(iPhaseName, iPhaseIdent, iX, iY, iMat, iEl, iUx, iUy, iUt, iPUx, iPUy, iPUt, iU1, iU2, iEffNormalStress, iTotNormalStress, iShearStress, iRelShearStress, iPExcess, iPActive, iPSteady, iPWater, iSuction, iEffSuction)])
        
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, x, y, mat, el, ux, uy, ut, pux, puy, put, u1, u2, ens, tns, ss, rss, pe, pa, pst, pw, su, esu in zip(iPhaseName, iPhaseIdent, iX, iY, iMat, iEl, iUx, iUy, iUt, iPUx, iPUy, iPUt, iU1, iU2, iEffNormalStress, iTotNormalStress, iShearStress, iRelShearStress, iPExcess, iPActive, iPSteady, iPWater, iSuction, iEffSuction):
                                     row = []
                                     row.append(pname)
                                     row.append(pident)
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
                                     row.append(ens)
                                     row.append(tns)
                                     row.append(ss)
                                     row.append(rss)
                                     row.append(pe)
                                     row.append(pa)
                                     row.append(pst)
                                     row.append(pw)
                                     row.append(su)
                                     row.append(esu)
                                     self.insertValues(row)
            
        print('getInterfaceResults Done')  
        
    def getSoilResultsByPoints(self,
                               filePoints=None,
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
            tableOut = 'getSoilResultsByPoints'
        
        locName = []
        locY = []
        locX = []
        
        MaterialID = []
        ElementID =[]
        
        Uyy = []
        Uxx = []
        Utot = []
            
        PUyy = []
        PUxx = []
        PUtot = []
        
        EffSxx = []
        EffSyy = []
        EffSzz = []
        
        EffP1 = []
        EffP2 = []
        EffP3 = []        
        
        PExcess = []
        PActive = []
        PSteady = []
        PWater = []
        
        Suct = []

        
        pPhaseName = []
        pPhaseIdent = []
               
        if filePoints:
            fpoint = open(filePoints, "r")

            while True:
                in_line = fpoint.readline()
                if in_line == "":
                    break
                print(in_line)
                [name, nx, ny] = in_line.split(',')
                self.NodeList.append(self.PointXY(name, nx, ny))

            fpoint.close()

       

        for phase in self.phaseOrder:
            print('Getting soil results ' + phase.Identification.value)
            

                       
            for pt in self.NodeList:

                try:
                    mat = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.MaterialID, (pt.x, pt.y))
                    el = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.ElementID, (pt.x, pt.y))
                    ux = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.Ux, (pt.x, pt.y))
                    uy = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.Uy, (pt.x, pt.y))
                    ut = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.Utot, (pt.x, pt.y))
                    pux = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.PUx, (pt.x, pt.y))
                    puy = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.PUy, (pt.x, pt.y))
                    put = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.PUtot, (pt.x, pt.y))
                    esx = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.SigxxE, (pt.x, pt.y))
                    esy = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.SigyyE, (pt.x, pt.y))
                    esz = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.SigzzE, (pt.x, pt.y))
                    ep1 = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.SigmaEffective1, (pt.x, pt.y))
                    ep2 = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.SigmaEffective2, (pt.x, pt.y))
                    ep3 = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.SigmaEffective3, (pt.x, pt.y))  
                    pe = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.PExcess, (pt.x, pt.y))
                    pa = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.PActive, (pt.x, pt.y))
                    ps = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.PSteady, (pt.x, pt.y))
                    pw = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.PWater, (pt.x, pt.y))
                    su = self.g_o.getsingleresult(phase, self.g_o.ResultTypes.Soil.Suction, (pt.x, pt.y))
                    
                    # print (pt.name, pt.x, pt.y, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su) 
                    
                    if ux != 'not found':
                    
                        pPhaseName.append(phase.Name.value)
                        pPhaseIdent.append(phase.Identification.value)
                    
                        locName.append(pt.name)
                        locY.append(pt.y)
                        locX.append(pt.x)
                        
                        MaterialID.append(int(float(mat) + .1))
                        ElementID.append(int(float(el) + .1))
                        
                        Uyy.append(uy)
                        Uxx.append(ux)
                        Utot.append(ut)
                        
                        PUyy.append(puy)
                        PUxx.append(pux)
                        PUtot.append(put)
                        
                        EffSxx.append (esx)
                        EffSyy.append (esy)
                        EffSzz.append (esz)
                           
                        EffP1.append (ep1)
                        EffP2.append (ep2)
                        EffP3.append (ep3)
                            
                        PExcess.append (pe)
                        PActive.append (pa)
                        PSteady.append (ps)
                        PWater.append (pw)
                        Suct.append (su)
                     
                except:
                    print ('...exception soil results ' + phase.Identification.value , pt.x, pt.y)
                    print (pt.name, pt.x, pt.y, mat, el, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su)
        columns = 'Phase,PhaseIdent,locName,locX(m),locY(m),MaterialID,ElementID,Ux(m),Uy(m),Utot(m),PUx(m),PUy(m),PUtot(m),SigxxEff(kPa),SigyyEff(kPa),SigzzEff(kPa),SigP1Eff(kPa),SigyP2Eff(kPa),SigP3Eff(kPa),PExcess(kPa),PActive(kPa),PSteady(kPa),Pwater(kPa),Suct(kPa)'  
        formats = '{},{},{},{:2f},{:2f},{:0},{:0},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f},{:2f}'
        
        if (fileOut == None and tableOut == None):
            columns += '\n'
            formats += '\n'
            print('Outputting to string....')
            rows = ''.join([formats.format(pname, pident, locname, float(x), float(y), mat, el, float(ux), float(uy), float(ut), float(pux), float(puy), float(put), float(esx), float(esy), float(esz), float(ep1), float(ep2), float(ep3), float(pe), float(pa), float(ps), float(pw), float(su))
                                     for pname, pident, locname, x, y, mat, el, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su in zip(pPhaseName, pPhaseIdent, locName, locX, locY, MaterialID, ElementID, Uxx, Uyy, Utot, PUxx, PUyy, PUtot, EffSxx, EffSyy, EffSzz, EffP1, EffP2, EffP3, PExcess, PActive, PSteady, PWater, Suct)])
            return columns + rows
        
        if (fileOut != None and tableOut == None):
            try :
                print('Outputting to file ', fileOut, '....')
                columns += '\n'
                formats += '\n'
                with open(fileOut, "w") as file:
                    file.writelines([columns])
                    file.writelines([formats.format(pname, pident, locname, float(x), float(y), mat, el, float(ux), float(uy), float(ut), float(pux), float(puy), float(put), float(esx), float(esy), float(esz), float(ep1), float(ep2), float(ep3), float(pe), float(pa), float(ps), float(pw), float(su))
                                     for pname, pident, locname, x, y, mat, el, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su in zip(pPhaseName, pPhaseIdent, locName, locX, locY, MaterialID, ElementID, Uxx, Uyy, Utot, PUxx, PUyy, PUtot, EffSxx, EffSyy, EffSzz, EffP1, EffP2, EffP3, PExcess, PActive, PSteady, PWater, Suct)])
            except:
                print ('...exception soil results ' + phase.Identification.value , pt.x, pt.y)
               #~ print (pname, pident, locname, x, y, mat, el, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su)
                #~ print (pPhaseName, pPhaseIdent, locName, locX, locY, MaterialID, ElementID, Uxx, Uyy, Utot, PUxx, PUyy, PUtot, EffSxx, EffSyy, EffSzz, EffP1, EffP2, EffP3, PExcess, PActive, PSteady, PWater, Suct)
        
        if (fileOut != None and tableOut != None):
            print('Outputting to database ', fileOut, '....')
            self.getConnected (fileOut)
            self.createTable(tableOut, columns, formats)
            for pname, pident, locname, x, y, mat, el, ux, uy, ut, pux, puy, put, esx, esy, esz, ep1, ep2, ep3, pe, pa, ps, pw, su in zip(pPhaseName, pPhaseIdent, locName, locX, locY, MaterialID, ElementID, Uxx, Uyy, Utot, PUxx, PUyy, PUtot, EffSxx, EffSyy, EffSzz, EffP1, EffP2, EffP3, PExcess, PActive, PSteady, PWater, Suct):
                row = []
                row.append(pname)
                row.append(pident)
                row.append(locname)
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
                row.append(esx)
                row.append(esy)
                row.append(esz)
                row.append(ep1)
                row.append(ep2)
                row.append(ep3)
                row.append(pe)
                row.append(pa)
                row.append(ps)
                row.append(pw)
                row.append(su)
                
                self.insertValues(row)
                
        print('getSoilResultsByPoint Done')
