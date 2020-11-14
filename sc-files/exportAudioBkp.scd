~audioFilename = "a";
~timestamp = "2018-03-22_23-30-06";
// for simplicity when editing this with python, the two first lines are the output filename and
// Timestamp, folder name where csv_data.txt is. Specific for each score/part.
// Don't edit this! Will break the python code and thus the whole process.


// SCRIPT FOR EXPORT AUDIO WITH NRT-SCSYNTH
//
//
// NRT export audio test

(
// ––––– SCORE DATA –––––
~sampleRate = 44100;
~lag = 1 / ~sampleRate;	// Lag: transition time between 0 and 1 in amplitude array.
//~lag = 0.001;



// ––––– GLOBAL VARS ––––––
// ––– (directories, names ++) –––
// –– csv directories ––

// TODO: GET PATH TO DIRECTORY
~csvDirectory = "" +/+ ~timestamp;
~csvFilepath = ~csvDirectory +/+ "csv_data.txt";
~csvHeaderFilepath = ~csvDirectory +/+ "csv_header.txt";

// –– oscScore ––
~oscScoreDir = "";
~oscscore = ~oscScoreDir +/+ "oscScore.osc";

// –– audioExport ––
~audioDir = "";
~audiofile = ~audioDir +/+ ~audioFilename ++ ".aiff";

// –– scsynth executable ––
~scsynthDir = "";

// OSC commands to instance of NRT-scynth
// "_" underscore means 'no input sound file needed'.
// -o 'number' refers to number of channels.
~cmd = "cd" + ~scsynthDir + "&& ./scsynth -N" + ~oscscore + "_" + ~audiofile + ~sampleRate.asString + "AIFF int24 -o 1";



// ––––– READING CSV –––––

// –––––––––– DATA COLLECTION AND DEFINITIONS ––––––––––
// –––––––––– (getting from CSV file and transforming ––
// –––––––––– to usable SC-data/arrays etc) ––––––––––––
//
// Opens file, read and put strings into array, close file.
// Flops array, so that equal values are in same array.
// Seperates header items from array of values.

// Reading CSV data to array:
// (Skips empty lines and blank entries cause by multiple commas)
// (Performing the same operation for the header file to get metadata on csv data.)
~csvData = CSVFileReader.read(~csvFilepath, true, true);
~csvHeaderFile = CSVFileReader.read(~csvHeaderFilepath, true, true);

// Adding header line to it's own array.:
~header = ~csvData.removeAt(0);
~csvHeaderFile_headerline = ~csvHeaderFile.removeAt(0);

// Transposing matrix. Equal type of values in their own arrays.
~csvData = ~csvData.flop;
~csvHeaderFile = ~csvHeaderFile.flop;

// Variables for arrays:
~durEnv = nil; ~shapes = nil; ~colors = nil; ~eventNums = nil;
~csvHeaderFile_framerate = nil; ~csvHeaderFile_numEvents = nil; ~csvHeaderFile_totalDuration = nil;

// Finding different data types in header, adding to their respectable arrays.
~header.do({arg item, idx; if(item == "event_num") {~eventNums = ~csvData[idx]};});
~header.do({arg item, idx; if(item == "color") {~colors = ~csvData[idx]};});
~header.do({arg item, idx; if(item == "shape") {~shapes = ~csvData[idx]};});
~header.do({arg item, idx; if(item == "duration") {~durEnv = ~csvData[idx]};});

// Also adding metadata from csv_header.txt to variables.
// Used for checking later in script
// (Assuming that there is only one line in csv-file after the header line, in which the data is written
// (therefore the 0 index. With this the variable holds not an array but a value.))
// (Also with interpret to convert any numbers from string to number)
~csvHeaderFile_headerline.do({arg item, idx; if(item == "framerate") {~csvHeaderFile_framerate = ~csvHeaderFile[idx][0].interpret};});
~csvHeaderFile_headerline.do({arg item, idx; if(item == "num_events") {~csvHeaderFile_numEvents = ~csvHeaderFile[idx][0].interpret};});
~csvHeaderFile_headerline.do({arg item, idx; if(item == "total_duration") {~csvHeaderFile_totalDuration = ~csvHeaderFile[idx][0].interpret};});

// Interpreting/converting numbers from strings to integers/floats.
// (Returns nil for all non-integers.)
// (Careful: interprets any non-number string as a symbol (variable name, class name, etc.))
~durEnv = ~durEnv.collect(_.interpret);
~eventNums = ~eventNums.collect(_.interpret);

// ----- PRINT content of lists -----
/*
(
~header.do(_.postln);
~eventNums.do(_.postln);
~colors.do(_.postln);
~shapes.do(_.postln);
~durEnv.do(_.postln);

~csvHeaderFile_framerate.postln;
~csvHeaderFile_numEvents.postln;
~csvHeaderFile_totalDuration.postln;
)
*/

// –––––––––– MAKE ENVELOPE ARRAYS ––––––––––
// Making amplitude envelope and adjusted duration envelope from csv arrays.
// so that they can be used in SynthDef.


// AMPLITUDE ENVELOPE
//
// Preparing amplitude envelope, to have values appended to it.
~ampEnv = [];

// Creating amplitude envelope from shapes.
// Also checking that colors and shapes are of equal length.
// Appends 0 to ampEnv where shape or color is None, appends 1 otherwise.
// (In other words: both color and shape must be non-nil/not None to append 1)

if (~colors.size == ~shapes.size, {
	~eventNums.do({arg item;
		if (~colors[item] == "None", // at colors[index]
			{~ampEnv = ~ampEnv.add(0)},		 // if None, add 0
			{~ampEnv = ~ampEnv.add(1)})		 // else, assume value and add 1
	})},
{"WARNING! Unequal length between shapes and colors list.".postln};);

// Make an amp envelope which can be read by a SynthDef
// and insert 0 at beginning (envelope starts always at 0).
~ampEnv = ~ampEnv.stutter(2).insert(0, 0);
~ampEnv = ~ampEnv.add(0);	// Insert 0 to always end at 0


// DURATION ENVELOPE
~durEnv = ~durEnv.stutter(2).collect(
	{arg item, idx;
		if(idx.mod(2) == 0)	// Doubling number of values (to fit with amp env)
		{~lag}				// If first value, start with lag
		{item - ~lag}});	// Then every second value duration - lag, and lag.
							// Sum of adjusted list should be equal to original duration list!
// To have lag also effect ending of envelope.
// Takes last value minus lag, and adds a last transition phase with lag duration.
// This to make sure that total duration does not get extended,
// but also makes a last lag/transition available.
~durEnv[~durEnv.size - 1] = ~durEnv[~durEnv.size-1] - ~lag;
~durEnv = ~durEnv.insert(~durEnv.size, ~lag);


// FOR PRINTING/CHECKING
/*
~ampEnv;
~durEnv;
~ampEnv.size.postln;
~durEnv.size.postln;	// Should be one less than ampEnv.
~durEnv.sum.postln;		// Should be equal to sum before adjustment.
*/



// ––––– SYNTHDEFS –––––
//
// Instance variables for synth:

/*
// TEST VARIABLES
~ampEnv = [0,1,0,1,0,1,0,1,0];
//~durEnv = [0.5, 0.5, 0.5, 0.5,0.5, 0.5, 0.5,0.5,0.5];
~durEnv = [0.25].stutter(~ampEnv.size - 1);
*/

~totalDuration = ~durEnv.sum.asFloat();

SynthDef(\testSynth,
	{	arg out=0, amp=0.5;
		var env, sig;
		env = Env(~ampEnv, ~durEnv);
		//env = Env([0,1,0],[1,1]);
		env = EnvGen.ar(env, doneAction:2);
		sig = SinOsc.ar(440, 0) * env;
		sig = sig * amp;
		sig.poll;
		Out.ar(out, sig!2);
}).writeDefFile;

// ––––– OSC SCORE –––––

~score = [
[0.0, [ \s_new, \testSynth, 1000, 0, 0, \amp, 1.0]],
[~totalDuration, [ \c_set, 0, 0]]
];

Score.write(~score, ~oscscore);


// Checking correspondancy between actual envelope duration and csv_header.txt total duration.
// Not running audio synthesis if not corresponding.

// Testing for correspondance between actual total duration (from duration envelope) and supposed total_duration (from metadata in csv_header.txt), with precision of one sample.
// If within precision, continue with generating audio file, if not, pass and post error message.
if ((~totalDuration.equalWithPrecision(~csvHeaderFile_totalDuration, (1.0 / ~sampleRate));),
	{
		"Success".postln;
		Routine {
			0.05.wait;
			"running cmd".postln;
			~result = ~cmd.unixCmd;
		}.play;

	},
	{"Error. Mismatching data. Exiting unsuccesfully".postln} )
)