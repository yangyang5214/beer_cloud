package com.beer.cloud_api.entity;


import lombok.Data;

@Data
public class FileEntity {

    private String name;
    private String date;
    private String size;
    private boolean dirFlag;
}
