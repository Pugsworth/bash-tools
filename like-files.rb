#!/usr/bin/env ruby

require "optparse";

$options = {
    :listmatches => true
};

def parseOptions(opts)
    optParser = OptionParser.new do |opt|
        opt.banner  = "Usage: like-files LEFT_PATH RIGHT_PATH [OPTIONS]";
        opt.separator "";
        opt.separator "Find files whose path is the same in another directory.";
        opt.separator "Default is to list files that exist in both directories."
        opt.separator "";
        opt.separator "Options";

        opt.on("-i", "--invert", "Invert results to show files not in RIGHT_PATH.") do
            $options[:listmatches] = false;
        end

        opt.on("-h", "--help", "Help") do
            puts optParser;
        end
    end

    # extract and remove defined options
    optParser.parse!;

    # serve help-text if no options given
    if ARGV.empty? then
        puts optParser;
        return false;
    end

    return true;
end

# path points to a directory and exists
def valid_path(dir)
    return File::exist?(dir) && File::directory?(dir);
end

def compare(left, right)

    # return if not valid_path(left) or not valid_path(right);

    Dir::foreach(left) do |entry|

        next if ['.', '..'].include? entry;

        left_entry = File::join(left, entry);
        right_entry = File::join(right, entry);

        right_exists = File::exist?(right_entry);

        if File::directory?(right_entry) then
            compare(left_entry, right_entry);
        else
            if $options[:listmatches] == true then
                puts right_entry if right_exists;
            else
                puts right_entry;
            end
        end

    end

end


def main()

    return if not parseOptions($options);

    dir_left  = ARGV[0];
    dir_right = ARGV[1];

    puts "Comparing #{dir_left} with #{dir_right}" if $stdout.isatty;

    compare(dir_left, dir_right);

end

main();
