// ByteBits (from Alejandro Olarte)

(
SynthDef(\byteBits,
{
	arg srMod=1.5, freq=11, amp=1.0;
	var sr = SampleRate.ir / srMod;
	var n = 16 ; //bit resolution
	var t = Phasor.ar(1,freq*((2**n)/sr),0,((2**n)-1)); //creating a raising value from 0 to 2**n
	//equations try one at the time
	var counter = LFDNoise0.ar(MouseY.kr(1,0.1),3.5,3.5);

	t = Select.ar(counter,[

	//t*(((t>>12)|(t>>8))&(63&(t>>4))),
	//t*(((t>>9)|(t>>13))&(25&(t>>6))),
	//t*(((t>>5)|(t>>8)) & 63),
	//t*(((t>>11)&(t>>8))&(123&(t>>3))),
	//t*(t>>8*((t>>15)|(t>>8))&(20|(t>>19)*5>>t|(t>>3))),		// !
	t*(t>>((t>>9)|(t>>8))&(63&(t>>4))),
	//(t>>7|t|t>>6)*10+4*(t&t>>13|t>>6),
	//t*t>>t>>t/3>>t**0.07&(t<<3>>t), 							// YEAH!
	//t * (t>>10	)|(t>>10)|(n<<t)
	//t * ((t>>n/3)|(t>>9)&(t**(n<<t)))|(n**2.718).reciprocal,
	//t * (t << 2) << t | 7 >> 13
	]);

	t = t % (2**(n)); // avoiding number beyond 2**(bit resolution)
	t = t*(0.5**(n-1)) - 1; //scaling to -1, 1
	t = t * amp;
	//t.poll;
	LeakDC.ar(t.dup);
}).writeDefFile;
);

(
Ndef(\srC, {		// Samplerate Control
	MouseY.kr(0.5, 10, 1, 0.05).poll;
});
Ndef(\freqC, {	// Frequency Control
	MouseX.kr(0.05, 1000, 1, 0.05).poll;
});
)

(
Ndef(\freqC).play;
Ndef(\srC).play;
)
Ndef(\byteBits).play;
Ndef(\byteBits).stop;

Ndef(\byteBits).set(\freq, 11);
Ndef(\byteBits).set(\srMod, 2);

// Map
Ndef(\byteBits).map(\srMod, Ndef(\srC), \freq, Ndef(\freqC));
Ndef(\byteBits).map(\freq, Ndef(\freqC));
Ndef(\byteBits).map(\srMod, Ndef(\srC));

Ndef(\byteBits).set(\srMod, nil, \freq, nil);
Ndef(\byteBits).set(\srMod, 1, \freq, 0.15);

