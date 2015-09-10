Tutorial
**************

In this basic tutorial, we'll see how we can use freqens to break some weak crypto. 


Scenario
----------
You are working for the NSA and find that some terrorists are using brainfuck programs to hack the whole universe.
Some intelligence lets you know that they are using extremely weak crypto (single byte xor) in order to "secure" their communications,
which you have been able to intercept. 

In particular, you want to decode a ciphertext that looks like this:

.. code::

   5  555 P55'P5     7PP&5V77V7P5V5V5&P77     55&P77&&&&55&P&5V7VV\x017P7&7P7V 7 P5V77 5&555V7V7P7V5P&P5      7&V5P7 5&V 
   777   5 5\x01++P&\x01++++P77 5&5&\x01++++++P77P&V55&\x01++++++++P77  5 5&\x01++++++++++P77&&5&55   
   7&\x01++++++++++++P77 5 55&&7&\x01++++++++++++++P77&5&5&\x01++++++++++++++++P77    5 55 7&\x01++++++++++++++++++P5&7&\x0
   1++++++++++++++++++++P77&5&5&\x01++++++++++++++++++++++P77&55&\x01++++++++++++++++++++++++P77   
   555&7&\x01++++++++++++++++++++++++++P77&&&&555  7&\x01++++++++++++++++++++++++++++P77  555 
   7&\x01++++++++++++++++++++++++++++++P5P&V7&\x01++++++++++++++++++++++++++++++++P77&555   
   7&\x01++++++++++++++++++++++++++++++++++P77&555&&7&\x01++++++++++++++++++++++++++++++++++++P77    5 55 
   7&\x01++++++++++++++++++++++++++++++++++++++P77P&V5&55  7&\x01++++++++++++++++++++++++++++++++++++++++P77     5 
   55&&7&\x01++++++++++++++++++++++++++++++++++++++++++P7&55  
   7\x01++++++++++++++++++++++++++++++++++++++++++++P77&55&\x01VVVVVVVVVVVVVVVVVVVVVV7P&55P77 55&V777P555 777&V7P555 
   777&VV55V\x015P&P&&&P&7VV5V5P   P7     5&&V5V 7  PP5     7&V7V55P&%5V


Getting an analyzer
----------------------
An analyzer represents the ideal frequency distribution your target plaintext has. Once it has been fed, it can be asked
to score strings based on how legit they seem (how similar its frequency distribution is to the analyzer's). There are several ways of building an analyzer.

* From a raw file: you can build an analyzer like
	.. code-block:: python

		from freqens.analyzer import Analyzer

		# a representative sample of the target frequency distribution 
		# ie. a normal brainfuck program
		filename = "./program.bf" 
		analyzer = Analyzer.from_raw_file(filename)

* From a frequency distribution file: which is a json file containing some absolute frequencies. \
	An example of a frequency distribution file would be:  
		.. code-block:: json

			{
				"a": 4,
				"b": 3
			}  

	This is how you build an analyzer from one of these files:
		.. code-block:: python

			from freqens.analyzer import Analyzer

			filename = "./bf-distribution.json"
			analyzer = Analyzer.from_file(filename)

* From a string:
	.. code-block:: python

		from freqens.analyzer import Analyzer

		analyzer = Analyzer("representative text")


For this scenario, the easiest way to build the bf analyzer is to use the ``freqens`` command line utility which lets you extract a frequency distribution file from an specified set of files. For example:
	.. code::

		$> cd my-bf-programs
		$> freqens *.bf > bf_frequency_distribution.json


Breaking the code
-------------------
Now that you know how to get a brainfuck analyzer, it's time to break the code. We'll decode the ciphertext with every possible key (as it is single byte xor, there's only 256 possible keys) and let the analyzer discover what is the real ciphertext. Our program will look like:

.. code-block:: python

	from freqens.analyzer import Analyzer

	def single_byte_xor(text, byte):
		return "".join( chr(c ^ byte) for c in bytearray(text) )

	with open("ciphertext.txt") as ciphertext_file:
		ciphertext = ciphertext_file.read()
		analyzer = Analyzer.from_file("bf_frequency_distribution.json")

		possible_plaintexts = ( single_byte_xor(ciphertext, byte) for byte in range(256) )

		answer = analyzer.choose_best(possible_plaintexts)

		print answer[0] # Solution !!!

And the program will print:

.. code-block:: brainfuck
	
	+++>++>>>+[>>,[>+++++<[[->]<<]<[>]>]>-[<<+++++>>-[<<---->>-[->]<]]
	<[<-<[<]+<+[>]<<+>->>>]<]<[<]>[-[>++++++<-]>[<+>-]+<<<+++>+>
	  [-
	    [<<+>->-
	      [<<[-]>>-
	        [<<++>+>-
	          [<<-->->>+++<-
	            [<<+>+>>--<-
	              [<<->->-
	                [<<++++>+>>+<-
	                  [>-<-
	                    [<<->->-
	                      [<<->>-
	                        [<<+++>>>-<-
	                          [<<---->>>++<-
	                            [<<++>>>+<-
	                              [>[-]<-
	                                [<<->>>+++<-
	                                  [<<->>>--<-
	                                    [<<++++>+>>+<-
	                                      [<<[-]>->>++<-
	                                        [<<+++++>+>>--<-
	                                          [<->>++<
	                                            [<<->>-
	]]]]]]]]]]]]]]]]]]]]]]<[->>[<<+>>-]<<<[>>>+<<<-]<[>>>+<<<-]]>>]
	>[-[---[-<]]>]>[+++[<+++++>--]>]+<++[[>+++++<-]<]>>[-.>]

Which is `obviously
<http://www.hevanet.com/cristofd/brainfuck/utm.b>`_ an Universal Turing Machine! Now you know terrorists have turing-complete technology in their hands.	