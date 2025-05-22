import netgen.meshing as meshing
import netgen.csg as csg
import ngsolve as ng

def MakeTStructureMesh(quads=True, nx1=4, ny1=4, nx2=4, ny2=4, ratio=0.5):
    mesh = meshing.Mesh()
    mesh.dim=3

    pids = []
    for i in range(ny1+1):
        for j in range(nx1+1):
            x,y,z = j/nx1, i/ny1, 0
            pids.append(mesh.Add (meshing.MeshPoint(csg.Pnt(x,y,z))))

    for i in range(1,ny2+1):
        for j in range(nx2+1):
            x,y,z = j/nx2, ratio, -i/ny2
            pids.append(mesh.Add (meshing.MeshPoint(csg.Pnt(x,y,z))))

    mesh.Add(meshing.FaceDescriptor(surfnr=1,domin=1,bc=1))
    
    for i in range(ny1):
        for j in range(nx1):
            base = i * (nx1+1) + j
            if quads:
                pnum = [base,base+1,base+nx1+2,base+nx1+1]
                elpids = [pids[p] for p in pnum]
                el = meshing.Element2D(1,elpids)
                mesh.Add(el)
            else:
                pnum1 = [base,base+1,base+nx1+1]
                pnum2 = [base+1,base+nx1+2,base+nx1+1]
                elpids1 = [pids[p] for p in pnum1]
                elpids2 = [pids[p] for p in pnum2]
                mesh.Add(meshing.Element2D(1,elpids1)) 
                mesh.Add(meshing.Element2D(1,elpids2))

    base1 = (ny1+1) * (nx1+1)

    for j in range(nx1):
        base = int(ny1/2) * (nx1+1) + j
        if quads:
            pnum = [base,base+1,base1+j+1,base1+j]
            elpids = [pids[p] for p in pnum]
            el = meshing.Element2D(1,elpids)
            mesh.Add(el)
        else:
            pnum1 = [base,base+1,base+nx1+1]
            pnum2 = [base+1,base+nx1+2,base+nx1+1]
            elpids1 = [pids[p] for p in pnum1]
            elpids2 = [pids[p] for p in pnum2]
            mesh.Add(meshing.Element2D(1,elpids1)) 
            mesh.Add(meshing.Element2D(1,elpids2))

    for i in range(1,ny2):
        for j in range(nx2):
            base = base1 + (i-1) * (nx2+1) + j
            if quads:
                pnum = [base,base+1,base+nx2+2,base+nx2+1]
                elpids = [pids[p] for p in pnum]
                el = meshing.Element2D(1,elpids)
                mesh.Add(el)
            else:
                pnum1 = [base,base+1,base+nx2+1]
                pnum2 = [base+1,base+nx2+2,base+nx2+1]
                elpids1 = [pids[p] for p in pnum1]
                elpids2 = [pids[p] for p in pnum2]
                mesh.Add(meshing.Element2D(1,elpids1)) 
                mesh.Add(meshing.Element2D(1,elpids2))

    for i in range(nx1):
        mesh.Add(meshing.Element1D([pids[i], pids[i+1]], index=1))
    for i in range(ny1):
        mesh.Add(meshing.Element1D([pids[i*(nx1+1)+nx1], pids[(i+1)*(nx1+1)+nx1]], index=2))
    for i in range(nx1):
        mesh.Add(meshing.Element1D([pids[ny1*(nx1+1)+i+1], pids[ny1*(nx1+1)+i]], index=3))
    for i in range(ny1):
        mesh.Add(meshing.Element1D([pids[(i+1)*(nx1+1)], pids[i*(nx1+1)]], index=4))

    for i in range(nx2):
        mesh.Add(meshing.Element1D([pids[int(ny1/2) * (nx1+1) + i], pids[int(ny1/2) * (nx1+1) + i+1]], index=5))

    mesh.Add(meshing.Element1D([pids[int(ny1/2) * (nx1+1)], pids[base1]], index=6))
    for i in range(ny2-1):
        mesh.Add(meshing.Element1D([pids[i*(nx2+1)+base1], pids[(i+1)*(nx2+1)+base1]], index=6))
    for i in range(nx2):
        mesh.Add(meshing.Element1D([pids[(ny2-1)*(nx2+1)+i+base1], pids[(ny2-1)*(nx2+1)+i+1+base1]], index=7))

    for i in range(ny2-1):
        mesh.Add(meshing.Element1D([pids[(i+1)*(nx2+1)+nx2+base1], pids[i*(nx2+1)+nx2+base1]], index=8))

    mesh.Add(meshing.Element1D([pids[base1+nx1], pids[int(ny1/2) * (nx1+1) + nx1]], index=8))
    
    mesh.SetCD2Name(1, "upbottom")        
    mesh.SetCD2Name(2, "upright")        
    mesh.SetCD2Name(3, "uptop")        
    mesh.SetCD2Name(4, "upleft")

    mesh.SetCD2Name(5, "interface")        
    mesh.SetCD2Name(6, "downright")        
    mesh.SetCD2Name(7, "downbottom")        
    mesh.SetCD2Name(8, "downleft")

    mesh.Compress()       
    ngsmesh = ng.Mesh(mesh)
    return ngsmesh