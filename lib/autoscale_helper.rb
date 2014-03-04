module EbsAutoscale
  module AutoscaleHelper
    def get_next_name(image_name, old_image_names)
      if old_image_names != nil
        last_idx = old_image_names.map { |s| s[/#{image_name}\-?(.*)/, 1].to_i(16) }.max || 0
        image_name = "#{image_name}-#{(last_idx+1).to_s(16)}"
      end
      image_name
    end

    def get_names_from_repository(base_name, repository)
      existing_names = {}
      repository.each_batch do |batch|
        existing_names.merge! Hash[batch.map{|i| [i.name, i]}.select { |name, i| name[/^#{base_name}/] }]
      end
      existing_names
    end

    def get_next_name_from_repository(base_name, repository)
      existing_names = get_names_from_repository(base_name, repository)
      [get_next_name(base_name, existing_names.keys), (existing_names.max_by { |k,_| k } || []).last ]
    end
  end
end