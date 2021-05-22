package com.beer.cloud_api.common;


import com.beer.cloud_api.entity.StoragePath;
import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
@Data
@ConfigurationProperties(prefix = "config")
public class StoragePathConfig {
    List<StoragePath> storages;
}
