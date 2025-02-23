package com.weaponwatch.adminapi.model;
import jakarta.persistence.*;

import java.util.Objects;

@Entity
public class Recording {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String filePath; // S3 key or file location

    public Recording(){}

    public Recording(Long id, String filePath){
        this.id = id;
        this.filePath = filePath;
    }

    // Getters & Setters
    public Long getId(){
        return id;
    }

    public String getFilePath(){
        return filePath;
    }

    public void setId(Long id){
        this.id = id;
    }

    public void setFiePath(String filePath){
        this.filePath = filePath;
    }

    @Override
    public boolean equals(Object o){
        if(this == o){
            return true;
        }
        if(!(o instanceof Recording)){
            return false;
        }
        Recording r = (Recording)o;
        return Objects.equals(r.id, this.id) && Objects.equals(r.filePath, this.filePath);
    }

    @Override
    public int hashCode(){
        return Objects.hash(this.id, this.filePath);
    }

    @Override
    public String toString(){
        return "Recording{" + "id: " + this.id + ", filePath:'" + this.filePath + "'}";
    }

}
