require_relative 'autoscale_helper'

Dir.glob(File.expand_path("../capistrano/tasks/*.cap", __FILE__)).each(&method(:load))