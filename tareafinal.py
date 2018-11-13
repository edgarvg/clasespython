
import cobra
import matplotlib.pyplot as plt
import numpy as np
from cobra.flux_analysis import production_envelope
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import cm

def main():
    model=cobra.io.read_sbml_model("iMT1026v3.xml")
    model.objective="Ex_biomass"
    #Definición Bounds
    
    #Methanol
    model.reactions.get_by_id("Ex_meoh").upper_bound=0
    model.reactions.get_by_id("Ex_meoh").lower_bound=-10
    #Glycerol
    model.reactions.get_by_id("Ex_glyc").upper_bound=0
    model.reactions.get_by_id("Ex_glyc").lower_bound=0
    #Glucosa
    model.reactions.get_by_id("Ex_glc_D").upper_bound=0
    model.reactions.get_by_id("Ex_glc_D").lower_bound=0
    #sorbitol exchange
    model.reactions.get_by_id("Ex_sbt_D").upper_bound=0
    model.reactions.get_by_id("Ex_sbt_D").lower_bound=0
    #Oxygen
    model.reactions.get_by_id("Ex_o2").upper_bound=0
    model.reactions.get_by_id("Ex_o2").lower_bound=-10
    #Generación datos plano de fase
    phase=cobra.flux_analysis.phenotype_phase_plane.production_envelope(model,['Ex_o2','Ex_meoh'], objective=model.objective)
    
    #Guardamos vectores del archivo pandas en un array
    o2=phase.iloc[:,7]
    meoh=phase.iloc[:,8]
    
    #Transformar columna de biomasa en matriz
    x=phase.iloc[:,3]
    x1=np.matrix(x.tolist())
    M=np.reshape(x1,[20,20])
    
    #Extraer los datos del flux de oxigeno
    
    a=np.zeros(20)
    for i in range (20):
        a[i]=o2[20*i]
        
    #Extraer los datos de flux de metanol
        
    b=np.zeros(20)    
    for i in range(20):
        b[i]=meoh[i]
        
            
    w=np.meshgrid(a,b)
    fig=plt.figure()
    ax=fig.gca(projection='3d')
    surf = ax.plot_surface(a, b, M, cmap=cm.coolwarm,linewidth=0, antialiased=False)
    ax.set_zlim(0,2)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.colorbar(surf,shrink=0.5,aspect=5)
    #plt.xlabel('Oxígeno')
    #plt.ylabel('Metanol')
    plt.show()
if __name__=="__main__":
    main()