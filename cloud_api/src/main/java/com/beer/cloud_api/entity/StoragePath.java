package com.beer.cloud_api.entity;


import lombok.Data;

import java.io.Serializable;

@Data
public class StoragePath implements Serializable {

    private String name;
    private String path;
    private String url;
}
