#Pi Piano

import pygame #for audio playback
import pygame.mixer as Mixer
import time #for delay at end of loop
import sys #for exit codes
import click #for command structure
import Adafruit_MPR121.MPR121 as MPR121 #hardware drivers

#Global Variables

#list of MPR121's used
TouchSensors = dict()
#audio file location maps
SOUND_MAPPING = [dict(), dict(), dict(), dict()]
SOUNDS = [ [0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0] ]

CHANNELS = [ [0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0] ]

def PlaySound(boardNum, pinNum):
    if SOUNDS[boardNum][pinNum]:
        CHANNELS[boardNum][pinNum].play(SOUNDS[boardNum][pinNum], -1)
    pass

def StopSound(boardNum, pinNum):
    CHANNELS[boardNum][pinNum].stop()
    pass

def LoadSoundFiles(InstrumentMap):
    click.echo("Loading Instruments")
    imf = open(InstrumentMap, 'r')
    fileCount = 0
    #for each file name in map file
    for fn in enumerate(imf):
        fp = str.strip(fn[1]) #strip whitespace from file path
        fnf = open(fp, 'r')
        #for each line in file
        for cnt, line in enumerate(fnf):
            line = str.strip(line) #strip whitespace at begin and end of line
            if cnt < 12:
                SOUND_MAPPING[fileCount][cnt] = line
                #click.echo("board " + str(fileCount) + " pin {" + str(cnt) + "} = " + line)
        fileCount += 1 #increment for next board

    #print debug info
    click.echo("\nInstruments loaded\n")
    
    pass
#end of LoadSoundFiles function

#initialize sounds & channels
def InitSoundChannel():
    click.echo("Setting up pygame mixer")
    #iterate through all sound mappings
    for listKey in range(0, 4):
        for dictKey, fileName in SOUND_MAPPING[listKey].items():
            #create sound object
            SOUNDS[listKey][dictKey] = pygame.mixer.Sound(fileName)
            SOUNDS[listKey][dictKey].set_volume(1)
            #create a channel for that sound
            channelID = (listKey * 12) + dictKey
            CHANNELS[listKey][dictKey] = Mixer.Channel(channelID)
    pass
#end of InitSoundChannel function

@click.command()
@click.argument('Instrument_Map', type=click.Path(exists=True))
@click.option('-a', is_flag=True)
@click.option('-b', is_flag=True)
@click.option('-c', is_flag=True)
@click.option('-d', is_flag=True)
def PiPiano(instrument_map, a, b, c, d):
    if a:
        click.echo("Attempting to register MPR121 on address 0x5A")
        TouchSensors[0] = MPR121.MPR121()
        if not (TouchSensors[0].begin(address=0x5A)):
            click.echo("*********************")
            click.echo("ERROR initializing MPR121 on address 0x5A")
            sys.exit(1)
        else:
            TouchSensors[0].set_thresholds(14, 8)
            click.echo("MPR121 on 0x5A initialized")
    if b:
        click.echo("Attempting to register MPR121 on address 0x5B")
        TouchSensors[1] = MPR121.MPR121()
        if not (TouchSensors[1].begin(address=0x5B)):
            click.echo("*********************")
            click.echo("ERROR initializing MPR121 on address 0x5B")
            sys.exit(1)
        else:
            TouchSensors[1].set_thresholds(14, 8)
            click.echo("MPR121 on 0x5B initialized")
    if c:
        click.echo("Attempting to register MPR121 on address 0x5C")
        TouchSensors[2] = MPR121.MPR121()
        if not (TouchSensors[2].begin(address=0x5C)):
            click.echo("*********************")
            click.echo("ERROR initializing MPR121 on address 0x5C")
            sys.exit(1)
        else:
            TouchSensors[2].set_thresholds(14, 8)
            click.echo("MPR121 on 0x5C initialized")
    if d:
        click.echo("Attempting to register MPR121 on address 0x5D")
        TouchSensors[3] = MPR121.MPR121()
        if not (TouchSensors[3].begin(address=0x5D)):
            click.echo("*********************")
            click.echo("ERROR initializing MPR121 on address 0x5D")
            sys.exit(1)
        else:
            TouchSensors[3].set_thresholds(14, 8)
            click.echo("MPR121 on 0x5D initialized")

    #initialize pygame mixer
    pygame.mixer.pre_init(44100, -16, 48, 512) #44.1khz, 16bit signed value, 12 channel, 512 bit biffer
    pygame.init()
    pygame.mixer.set_num_channels(48) # doesn't seem to stick in pre_init
    click.echo("Mixer setup.  Number of channels = " + str(pygame.mixer.get_num_channels()))

    
    click.echo("\nInstrument map file:")
    click.echo(str(instrument_map))
    LoadSoundFiles(instrument_map)
    InitSoundChannel()

    #print(SOUND_MAPPING) #DEBUG verify variable scope worked correctly
    
    click.echo("\nMPR List:")
    click.echo(str(TouchSensors))
    
    #initialize previous state of sensors
    click.echo("\nInitializing Touch memory.")
    last_touched = [0,0,0,0]
    current_touched = [0,0,0,0]
    for boardNum, MPR in TouchSensors.items():
        last_touched[boardNum] = MPR.touched()
        #print(last_touched[boardNum])

    click.echo("Memory initialized.  Starting main loop...")
    click.echo("Press Ctrl-C to quit.")
    #start main loop
    while True:
        
        for boardNum, MPR in TouchSensors.items():
            
            current_touched[boardNum] = MPR.touched()
            
            CurStat = "Board " + str(boardNum) + " status = " + str(current_touched[boardNum])
            LastStat = "  Last touched = " + str(last_touched[boardNum])
            #click.echo(CurStat + LastStat)
            
            #click.echo("Board " + str(boardNum) + " touched: " + str(current_touched))
            for pinNum in range(12):
                pin_bit = 1 << pinNum

                #click.echo("Checking pin " + str(pinNum) + " on board " + str(boardNum))
                
                #get boolean-compatible values for current& last state
                CurState = current_touched[boardNum] & pin_bit
                LastState = last_touched[boardNum] & pin_bit
                
                #if now touching
                if (current_touched[boardNum] & pin_bit and not last_touched[boardNum] & pin_bit):
                    click.echo("Board " + str(boardNum) + " pin " + str(pinNum) + " is touching.")
                    #play sound
                    PlaySound(boardNum, pinNum)
                #if now releasing
                if (not current_touched[boardNum] & pin_bit and last_touched[boardNum] & pin_bit):
                    click.echo("Board " + str(boardNum) + " pin " + str(pinNum) + " is released.")
                    #stop sound
                    StopSound(boardNum, pinNum)

            #remember touched value for next time
            last_touched[boardNum] = current_touched[boardNum]
        #end for loop
        
        #delay loop
        time.sleep(0.1)
    #end main loop
    
    
    click.echo("\nEnd of PiPiano Program.\n")
#end PiPiano Function

#main program execution
if __name__ == '__main__':
    click.echo("***** Welcome to the Raspberry Pi Piano Program *****")
    click.echo(" Powered by Adafruit MPR121 Capacitive Touch Sensors ")
    click.echo("")
    PiPiano()
    
    #pass
#end main
