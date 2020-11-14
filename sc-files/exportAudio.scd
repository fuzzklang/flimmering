// SCRIPT FOR EXPORT AUDIO WITH NRT-SCSYNTH
//
//
// NRT export audio test

(
// ––––– SCORE DATA –––––
//
// Fetching data from text file written by Python (rewritten for each run).
// First line is timestamp (which is needed to find csv-files)
// Second line is name of audio output file.
// Third line is amplitude of synth
// Fourth line tells script to map sound-configurations in synth either to colors or shapes.

// TODO: GET PATH TO DIRECTORY

~datafile = FileReader.read(~projectDirectory +/+ "score_files/run_data/run_data.txt", true); // If file not in this directory, the code breaks.

~timestamp = ~datafile[0][0];
~audioFilename = ~datafile[1][0];
~globalAmp = ~datafile[2][0];
~mappingKey = ~datafile[3][0];

~globalAmp = ~globalAmp.interpret;


~sampleRate = 44100;
~lag = 1 / ~sampleRate;	// Lag: transition time between 0 and 1 in amplitude array.
//~lag = 0.001;



// ––––– GLOBAL VARS ––––––
// ––– (directories, names ++) –––
// –– csv directories ––
~csvDirectory = ~projectDirectory +/+ "csv_export_data/" +/+ ~timestamp;
//~testDirectory = ""; ~csvDirectory = ~testDirectory;
~csvFilepath = ~csvDirectory +/+ "csv_data.txt";
~csvHeaderFilepath = ~csvDirectory +/+ "csv_header.txt";


// –– oscScore ––
~oscScoreDir = ~projectDirectory +/+ "oscscores";
~oscscore = ~oscScoreDir +/+ "oscScore.osc";

// –– audioExport ––
~audioDir = ~projectDirectory +/+ "audio/";
~audiofile = ~audioDir +/+ ~audioFilename ++ ".aiff";

// –– scsynth executable ––

// GET PATH TO EXECUTABLE
~scsynthDir = "";


// OSC commands to instance of NRT-scynth
// "_" underscore means 'no input sound file needed'.
// -o 'number' refers to number of channels.
~cmd = "cd" + ~scsynthDir + "&& ./scsynth -N" + ~oscscore + "_" + ~audiofile + ~sampleRate.asString + "AIFF int24 -o 2";



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


// –––––––––– SHAPE/COLOR ENVELOPES ––––––––––
// Envelopes, where color or shape gets translated (through a translation table) to indexes
// which decides which byte bit formula to pick.
~translationTable = Dictionary.newFrom(List["R", 0, "G", 1, "B", 2, "CIRCLE", 0, "CIRCLE", 1, "RECTANGLE", 2]);

// Checking whether to map sound-configurations from colors or shapes.

case {~mappingKey == "color"} {
	~counterList = Array.new(~colors.size);
	~colors.do({arg color; if (color != "None")
		{~counterList.add(~translationTable.at(color.toUpper))}});}
	{~mappingKey == "shape"} {
		~counterList = Array.new(~shapes.size);
		~shapes.do({arg shape; if (shape != "None")
			{~counterList.add(~translationTable.at(shape.toUpper))}});
	}
	{~mappingKey == "None"} {
	~counterList = Array.new(~colors.size);
	~colors.do({arg color; if (color != "None")
		{~counterList.add(0)}})
	};


~translationTableParams = Dictionary.newFrom(List["0", [0.7, 4.8], "1", [0.3, 1], "2", [6, 9]]);
~srMods = ~counterList.collect({arg item; ~translationTableParams.at(item.asString)[0]});
~freqs = ~counterList.collect({arg item; ~translationTableParams.at(item.asString)[1]});


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
		//sig.poll;
		Out.ar(out, sig!2);
}).writeDefFile;


SynthDef(\byteBits,
	{
		arg amp=1.0, out=0;
		//srMod=0.7, freq=4.8
		var env, demandUgen, counter, sr, srMod, freq;
		var n = 16 ; //bit resolution
		var t;
		//equations try one at the time
		//var counter = LFDNoise0.ar(MouseY.kr(1,0.1),3.5,3.5);
		env = Env(~ampEnv, ~durEnv);

		env = EnvGen.ar(env, doneAction:2);
		env.poll;

		counter = Dseq(~counterList, inf);
		counter = Demand.ar(env, 0, counter);

		srMod = Dseq(~srMods, inf);
		srMod = Demand.ar(env, 0, srMod);
		sr = SampleRate.ir / srMod;

		freq = Dseq(~freqs, inf);
		freq = Demand.ar(env, 0, freq);

		t = Phasor.ar(1,freq*((2**n)/sr),0,((2**n)-1)); //creating a raising value from 0 to 2**n

		t = Select.ar(counter,[
			t*(((t>>5)|(t>>8)) & 63),
			t*(t>>8*((t>>15)|(t>>8))&(20|(t>>19)*5>>t|(t>>3))),		// !
			t*t>>t>>t/3>>t**0.07&(t<<3>>t), 						// YEAH!

			//t*(((t>>12)|(t>>8))&(63&(t>>4))),
			//t*(((t>>9)|(t>>13))&(25&(t>>6))),
			//t*(((t>>11)&(t>>8))&(123&(t>>3))),
			//t*(t>>((t>>9)|(t>>8))&(63&(t>>4))),
			//(t>>7|t|t>>6)*10+4*(t&t>>13|t>>6),
			//t * (t>>10	)|(t>>10)|(n<<t)
			//t * ((t>>n/3)|(t>>9)&(t**(n<<t)))|(n**2.718).reciprocal,
			//t * (t << 2) << t | 7 >> 13
		]);

		t = t % (2**(n)); // avoiding number beyond 2**(bit resolution)
		t = t*(0.5**(n-1)) - 1; //scaling to -1, 1
		t = t * amp * env;
		t = LeakDC.ar(t);
		t = HPF.ar(t, 40);
		t = HPF.ar(t, 35);
		t = HPF.ar(t, 30);
		t = HPF.ar(t, 30);
		t = HPF.ar(t, 30);
		t = HPF.ar(t, 30);
		//t.poll;
		Out.ar(out, t!2);
}).writeDefFile;
//}).add;




// ––––– OSC SCORE –––––

~score = [
[0.0, [ \s_new, \byteBits, 1000, 0, 0, \amp, ~globalAmp]],
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
			0.1.wait;
			"running cmd".postln;
			~result = ~cmd.unixCmd;
			"RESULT".postln;
			~result.postln;
			2.0.wait;
			"killall sclang".unixCmd;
		}.play;

	},
	{"Error. Mismatching data. Exiting unsuccesfully".postln} );

"End of script, what the fuck is happening from here?".postln;
)



 // FOR TESTING

/*
~ampEnv
~durEnv
~counterList
~srMods
~freqs
*/