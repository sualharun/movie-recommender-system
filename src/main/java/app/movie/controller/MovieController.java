package app.movie.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.ResponseEntity;
import java.util.Map;
import java.util.HashMap;

@RestController
@RequestMapping("/api/movies")
@CrossOrigin(origins = "*")
public class MovieController {

    @Autowired
    private RestTemplate restTemplate;

    private static final String RECOMMENDER_SERVICE_URL = "http://localhost:5001/recommend";

    @GetMapping("/recommend")
    public ResponseEntity<?> getRecommendations(@RequestParam String movie) {
        try {
            String url = RECOMMENDER_SERVICE_URL + "?movie=" + movie;
            @SuppressWarnings("unchecked")
            Map<String, Object> response = restTemplate.getForObject(url, Map.class);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("error", "Recommendation service unavailable");
            errorResponse.put("message", "Please make sure the Python API is running on port 5001");
            return ResponseEntity.ok(errorResponse);
        }
    }
}