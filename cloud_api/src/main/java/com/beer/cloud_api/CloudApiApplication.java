package com.beer.cloud_api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;


@SpringBootApplication
@RestController
public class CloudApiApplication {


    public static void main(String[] args) {
        SpringApplication.run(CloudApiApplication.class, args);
    }


    @GetMapping("about")
    public String about() {
        return "beer cloud api";
    }

}
