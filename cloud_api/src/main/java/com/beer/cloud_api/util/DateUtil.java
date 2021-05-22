package com.beer.cloud_api.util;


import java.text.DateFormat;
import java.util.Date;
import java.util.Locale;

public class DateUtil {

    private static DateFormat dateFormat = DateFormat.getDateInstance(DateFormat.LONG, Locale.CHINA);

    public static String formatDate(Date date) {
        return dateFormat.format(date);
    }

    public static void main(String[] args) {
        System.out.println(formatDate(new Date()));
    }
}
