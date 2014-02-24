$LOAD_PATH.unshift 'lib'
require "ebs_autoscale/version"
 
Gem::Specification.new do |s|
  s.name = "ebs-autoscale"
  s.version = EBSAutoscale::VERSION
  s.date = Time.now.strftime('%Y-%m-%d')
  s.summary = "Feed me."
  s.homepage = "http://github.com/uriagassi/ebs-autoscale"
  s.email = "uri.agassi@gmail.com"
  s.authors = [ "Uri Agassi" ]
  s.has_rdoc = false

  s.files = %w( README.md Rakefile LICENSE )
  s.files += Dir.glob("lib/**/*")
  s.files += Dir.glob("bin/**/*")

# s.executables = %w( ebs-autoscale )
  s.description = <<desc
Feed me.
desc

  s.add_dependency 'capistrano', '>=3.0.1'
  s.add_dependency 'aws-sdk', '>=1.8.5'
end
