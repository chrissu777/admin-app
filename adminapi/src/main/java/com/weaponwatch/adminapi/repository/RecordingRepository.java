package com.weaponwatch.adminapi.repository;
import com.weaponwatch.adminapi.model.Recording;
import org.springframework.data.jpa.repository.JpaRepository;

public interface RecordingRepository extends JpaRepository<Recording, Long> {
}
