#!/usr/bin/perl

use strict;
use warnings;
use Carp;
use Text::CSV;
use GD::Graph::bars;

# Parse CSV file and convert the data for the
# requested $type and $date into a list of [X,Y] pairs.
my $folder = "\Users\Yun Jung\Desktop\SP 2014\BIMM 185\project";
my @filenames = ("204252_at", "211803_at");
my ($csv_file, $type, $date) = @ARGV;
my @xy_points;
my %i = ( X => -1, Y => -1 );
open(my $csv_fh, '<', $csv_file) or die $!;
my $parser = Text::CSV->new();
$parser->column_names( $parser->getline($csv_fh) );
while ( defined( my $hr = $parser->getline_hr($csv_fh) ) ){
    next unless $hr->{type} eq $type;
    my $xy = $hr->{site};
    $xy_points[++ $i{$xy}][$xy eq 'X' ? 0 : 1] = $hr->{$date};

# create new image
my $graph = new GD::Graph::bars(600, 500);
    
# discover maximum values of x and y for graph parameters
my( $xmax) = sort {$b <=> $a} keys %dataset;
my( $ymax) = sort {$b <=> $a} values %dataset;
# how many ticks to put on y axis
my $yticks = int($ymax / 5) + 1;
    
# define input arrays and enter 0 if undefined x value
my(@xsizes) = (0 .. $xmax);
my(@ycounts) = ();
foreach my $x (@xsizes) {
    if ( defined $dataset{$x}) {
        push @ycounts, $dataset{$x};
    }else{
        push @ycounts, 0;
    }
}

# set parameters for graph
$graph->set(
    transparent                => 0,
    title                => "Obese & non-Obese data",
    x_label                => 'Name of tissue',
    y_label                => '204252_at',
    x_all_ticks                => 1,
    y_all_ticks                => 0,
    y_tick_number        => $yticks,
    zero_axis                => 0,
    zero_axis_only        => 0,
);
    
# plot the data on the graph
my $gd = $graph->plot(
    [ xsizes,
      ycounts
    ]
);

# output file
my $pngfile = "gdgraph1.png";
unless(open(PNG, ">$pngfile")) {
    croak "Cannot open $pngfile:$!\n";
}

# set output file handle PNG to binary stream
# (this is important sometimes, for example doing
# GCI programming on some operating systems
binmode PNG;

# print the image to the output file
print PNG $gd->png;
