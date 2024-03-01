#! /usr/bin/perl
use FileHandle;
use IPC::Open2;

if($#ARGV!=1)
{
  print "USAGE: driver.pl blackplayer whiteplayer\n"; 
}
else
{

    system("rm -f .newgame.txt");
    system("rm -f D5.txt");
    system("rm -f E4.txt");

    $aaa = "echo \"BWBWBWBW\nWBWBWBWB\">>.newgame.txt";
    system($aaa);
    system($aaa);
    system($aaa);
    system($aaa);

    $pid1 = open2( \*Reader1,\*Writer1, "python3 $ARGV[0] .newgame.txt B" );
    Writer1->autoflush(); 
    $ll=<Reader1>;
    print "B:";
    print $ll;
    $aaa = "python3 knmv.py .newgame.txt B " . $ll;
    system($aaa);
    if($?!=0) {exit()};
    $pid2 = open2( \*Reader2,\*Writer2, "python3 $ARGV[1] .newgame.txt W" );
    Writer2->autoflush(); 
    for($i=0;$i<=33;$i++)
    {
       $ll=<Reader2>;
       print "W:";
       print $ll;
       $aaa = "python3 knmv.py .newgame.txt W " . $ll;
       system($aaa); 
       if($?!=0) {exit()};
       print Writer1 $ll;
       $ll=<Reader1>;
       print "B:";
       print $ll;
       $aaa = "python3 knmv.py .newgame.txt B " . $ll;
       system($aaa);
       if($?!=0) {exit()};       
       print Writer2 $ll;
    }
 system("rm -f .newgame.txt"); 
 }
