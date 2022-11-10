# run variables
VISU_DIR="visualisation"

#command line arguments
args=("$@")
CLA_VISUALISATION=${args[0]} # expects "vis" or "no_vis"
CLA_OUTPUT_DIR=${args[1]} 

VISU_OUTPUT_DIR="${CLA_OUTPUT_DIR}/${VISU_DIR}"

# visualization (video with paraview)
if [ "$CLA_VISUALISATION" = "vis" ];
then
    echo AUTOMATED VISUALISATION still broken... SORRYYYY
    echo starting visualisation at $(date)
    # check whether visualisation folder exists else define
    if [ ! -d $VISU_OUTPUT_DIR ]
    then
        mkdir $VISU_OUTPUT_DIR
        #echo ...$VISU_OUTPUT_DIR folder is created
    fi

    # run visualisation script(s)
    pvpython ../scripts_visualisation/try_paraview_automatisierung_screenshotgeneration_no_streamlines.py $CLA_OUTPUT_DIR $VISU_OUTPUT_DIR
    ## video only if enough pictures are outputted
    #pvpython ../scripts_visualisation/try_paraview_automatisierung_videogeneration.py $CLA_OUTPUT_DIR $VISU_OUTPUT_DIR
    #pvpython ../scripts_visualisation/try_paraview_automatisierung_screenshotgeneration.py $CLA_OUTPUT_DIR $VISU_OUTPUT_DIR
    echo finished paraview visualisation at $(date)
#else
#    echo no visualisation performed and saved
fi