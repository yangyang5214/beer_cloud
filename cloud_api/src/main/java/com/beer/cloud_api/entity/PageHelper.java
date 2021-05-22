package com.beer.cloud_api.entity;

import lombok.Data;

import java.util.List;

@Data
public class PageHelper<T> {

    private int page;
    private int pageSize;
    private int total;
    private List<T> data;

    public PageHelper() {
    }

    public PageHelper(int page, int pageSize, int total, List<T> data) {
        this.page = page;
        this.pageSize = pageSize;
        this.total = total;
        this.data = subList(data);
    }

    public List<T> subList(List<T> list) {
        if (page < 0) {
            page = 1;
        }
        int size = list.size();
        int start = (page - 1) * pageSize;
        if (start > size) {
            return null;
        }
        int end = start + pageSize;
        if (end > size) {
            return list.subList(start, size);
        }
        return list.subList(start, end);
    }
}
