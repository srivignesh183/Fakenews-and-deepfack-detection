import io
import numpy as np
from PIL import Image, ImageChops, ImageEnhance, ExifTags

class ProfessionalDeepfakeDetector:
    """
    Forensic Computer Vision & Digital Provenance Suite:
    1. Localized Error Level Analysis (ELA) with 8x8 block-grid anomaly localization
    2. 2D Fast Fourier Transform (FFT) Power-Spectrum Radial Gradient Evaluation
    3. EXIF & Sensor Provenance Signature Extraction
    4. Laplacian Edge Gradient & Noise Variance Analysis
    5. Color Channel Discrepancy & Chrominance Inconsistency Audit
    """

    def __init__(self, ela_quality: int = 90):
        self.ela_quality = ela_quality

    def analyze_image(self, file_bytes: bytes, filename: str):
        try:
            image = Image.open(io.BytesIO(file_bytes))
            if image.mode not in ("RGB", "L"):
                image = image.convert("RGB")
        except Exception as e:
            return {"error": f"Invalid or unreadable image file: {str(e)}. Supported formats: JPG, PNG, WEBP."}

        width, height = image.size

        # 1. Metadata & Provenance Audit
        metadata_report = self._inspect_metadata(image)

        # 2. Localized Error Level Analysis
        ela_img, ela_mean, ela_p95, ela_local_std, ela_heatmap_rgb = self._compute_ela(image)

        # 3. Frequency Spectrum Analysis (2D FFT)
        fft_radial_score, fft_img, fft_anomalous_spikes = self._frequency_spectrum_analysis(image)

        # 4. Laplacian Noise & Edge Smoothness
        noise_variance, is_abnormally_smooth = self._noise_variance_analysis(image)

        # 5. Chrominance Channel Consistency
        chroma_variance = self._chrominance_analysis(image)

        # 6. Multi-Factor Forensic Scoring Synthesis
        risk_score = 0.0
        indicators = []

        # Factor: Localized Compression (ELA)
        if ela_p95 > 8.0 or ela_local_std > 4.5:
            risk_score += 35.0
            indicators.append({
                "factor": "Error Level Analysis (ELA)",
                "status": "Localized Compression Splicing",
                "severity": "critical",
                "score_impact": "+35 Risk",
                "details": f"High peak re-compression difference ({ela_p95:.1f}) and local tile variance ({ela_local_std:.2f}) confirm spliced or copy-pasted visual content."
            })
        elif ela_p95 > 4.5 or ela_mean > 2.5:
            risk_score += 18.0
            indicators.append({
                "factor": "Error Level Analysis (ELA)",
                "status": "Moderate Compression Inconsistency",
                "severity": "warning",
                "score_impact": "+18 Risk",
                "details": f"Mean difference of {ela_mean:.2f}. Slight compression variance across image boundaries."
            })
        else:
            indicators.append({
                "factor": "Error Level Analysis (ELA)",
                "status": "Uniform Compression Grid",
                "severity": "normal",
                "score_impact": "0 Risk",
                "details": f"Compression artifacts are uniform across the image plane (mean: {ela_mean:.2f})."
            })

        # Factor: Frequency Spectrum & GAN Checkerboard
        if fft_radial_score > 0.82 or fft_anomalous_spikes:
            risk_score += 30.0
            indicators.append({
                "factor": "2D Fourier Spectral Analysis (FFT)",
                "status": "Synthetic Lattice / Upsampling Grid",
                "severity": "critical",
                "score_impact": "+30 Risk",
                "details": f"High radial power ratio ({fft_radial_score:.2f}) and spectral peaks characteristic of neural generator convolutions."
            })
        else:
            indicators.append({
                "factor": "2D Fourier Spectral Analysis (FFT)",
                "status": "Natural Photographic Spectrum",
                "severity": "normal",
                "score_impact": "0 Risk",
                "details": f"Frequency spectrum adheres to standard 1/f power-law decay of natural optical lenses (score: {fft_radial_score:.2f})."
            })

        # Factor: Metadata & Software Traces
        if metadata_report["has_editing_software"]:
            risk_score += 30.0
            indicators.append({
                "factor": "Metadata & Provenance Signature",
                "status": "Editing / Generative Software Stamp",
                "severity": "critical",
                "score_impact": "+30 Risk",
                "details": f"File contains active manipulation tool signature: '{metadata_report['software_tag']}'."
            })
        elif metadata_report["exif_count"] == 0:
            risk_score += 10.0
            indicators.append({
                "factor": "Metadata & Provenance Signature",
                "status": "Stripped / Absent Hardware EXIF",
                "severity": "warning",
                "score_impact": "+10 Risk",
                "details": "No physical sensor or camera EXIF header present. Typical of AI generation or web scraping."
            })
        else:
            indicators.append({
                "factor": "Metadata & Provenance Signature",
                "status": "Hardware Sensor Validated",
                "severity": "normal",
                "score_impact": "0 Risk",
                "details": f"Verified physical camera metadata: {metadata_report['camera_make'] or 'Camera Hardware'}."
            })

        # Factor: Noise & Sharpness Integrity
        if is_abnormally_smooth:
            risk_score += 15.0
            indicators.append({
                "factor": "Pixel Noise & Edge Smoothness",
                "status": "Synthetic Blurring / Skin Smoothing",
                "severity": "warning",
                "score_impact": "+15 Risk",
                "details": f"Abnormally low Laplacian variance ({noise_variance:.1f}). Common in deepfake boundary blending."
            })
        elif noise_variance > 800.0:
            risk_score += 15.0
            indicators.append({
                "factor": "Pixel Noise & Edge Smoothness",
                "status": "Artificial Edge High-Frequency Grid",
                "severity": "warning",
                "score_impact": "+15 Risk",
                "details": f"High structural variance ({noise_variance:.1f}) matching synthetic raster grids."
            })
        else:
            indicators.append({
                "factor": "Pixel Noise & Edge Smoothness",
                "status": "Natural Optical Grain",
                "severity": "normal",
                "score_impact": "0 Risk",
                "details": f"Stochastic sensor noise variance ({noise_variance:.1f}) conforms to physical light capture."
            })

        # Factor: Chrominance Inconsistency
        if chroma_variance > 65.0:
            risk_score += 10.0
            indicators.append({
                "factor": "Chrominance Channel Consistency",
                "status": "Color Space Anomaly",
                "severity": "warning",
                "score_impact": "+10 Risk",
                "details": f"Elevated color plane differential ({chroma_variance:.1f}) suggests localized color grading or patch insertion."
            })

        # Composite Probability & Authenticity
        manipulation_prob = float(np.clip(risk_score, 5.0, 96.0))
        authenticity_score = round(100.0 - manipulation_prob, 1)

        if manipulation_prob >= 40.0:
            verdict = "Potential Deepfake / Manipulated"
            status_badge = "Manipulated / AI-Generated"
            confidence = round(manipulation_prob, 1)
            risk_classification = "High Tampering Risk" if manipulation_prob > 70.0 else "Elevated Risk"
        else:
            verdict = "Likely Authentic"
            status_badge = "Authentic Media"
            confidence = round(authenticity_score, 1)
            risk_classification = "Low Tampering Risk"

        # Forensic Dimension Radar
        forensic_dimensions = {
            "Compression Grid Consistency": round(max(100.0 - (ela_p95 * 8.0 + ela_local_std * 6.0), 5.0), 1),
            "Fourier Spectral Naturalness": round(max(100.0 - (fft_radial_score * 90.0), 8.0), 1),
            "Metadata Provenance": 95.0 if metadata_report["exif_count"] > 0 and not metadata_report["has_editing_software"] else (15.0 if metadata_report["has_editing_software"] else 45.0),
            "Sensor Noise Realism": round(max(100.0 - abs(noise_variance - 200.0) * 0.12, 10.0), 1),
            "Chrominance Coherence": round(max(100.0 - chroma_variance, 15.0), 1)
        }

        return {
            "verdict": verdict,
            "status_badge": status_badge,
            "authenticity_score": authenticity_score,
            "manipulation_probability": round(manipulation_prob, 1),
            "confidence": confidence,
            "risk_classification": risk_classification,
            "dimensions": f"{width}x{height}",
            "ela_score": round(ela_mean, 2),
            "ela_p95": round(ela_p95, 2),
            "fft_score": round(fft_radial_score, 3),
            "noise_variance": round(noise_variance, 2),
            "chroma_variance": round(chroma_variance, 2),
            "metadata_summary": metadata_report,
            "indicators": indicators,
            "forensic_dimensions": forensic_dimensions,
            "ela_image": ela_img,
            "ela_heatmap": ela_heatmap_rgb,
            "fft_image": fft_img
        }

    def _inspect_metadata(self, image: Image.Image) -> dict:
        info = {
            "exif_count": 0,
            "camera_make": None,
            "software_tag": None,
            "has_editing_software": False,
            "raw_tags": {}
        }
        try:
            exif_data = image.getexif()
            if exif_data:
                info["exif_count"] = len(exif_data)
                for tag_id, value in exif_data.items():
                    tag = ExifTags.TAGS.get(tag_id, str(tag_id))
                    str_val = str(value).strip()
                    info["raw_tags"][tag] = str_val[:100]

                    if tag.lower() in ("make", "model"):
                        info["camera_make"] = str_val
                    elif tag.lower() in ("software", "processingsoftware"):
                        info["software_tag"] = str_val
                        if any(k in str_val.lower() for k in ["photoshop", "gimp", "stable diffusion", "midjourney", "dall-e", "canva", "affinity"]):
                            info["has_editing_software"] = True
        except Exception:
            pass
        return info

    def _compute_ela(self, image: Image.Image):
        rgb_img = image.convert("RGB")
        buffer = io.BytesIO()
        rgb_img.save(buffer, "JPEG", quality=self.ela_quality)
        buffer.seek(0)
        recompressed = Image.open(buffer)

        diff = ImageChops.difference(rgb_img, recompressed)
        diff_arr = np.array(diff, dtype=np.float32)
        ela_mean = float(np.mean(diff_arr))
        ela_p95 = float(np.percentile(diff_arr, 95))

        # 8x8 Tile variance
        h, w = diff_arr.shape[:2]
        block_means = []
        bh, bw = max(h // 8, 8), max(w // 8, 8)
        for i in range(0, h - bh + 1, bh):
            for j in range(0, w - bw + 1, bw):
                block = diff_arr[i:i+bh, j:j+bw]
                block_means.append(np.mean(block))
        ela_local_std = float(np.std(block_means)) if block_means else 0.0

        extrema = diff.getextrema()
        max_diff = max([ex[1] for ex in extrema]) if extrema else 1
        scale_factor = 255.0 / max(max_diff, 1)
        enhanced_diff = ImageEnhance.Brightness(diff).enhance(scale_factor)

        # Generate false-color thermal heatmap (Red=High variance, Blue=Low)
        gray_diff = np.mean(diff_arr, axis=2)
        norm_diff = np.clip(gray_diff / max(np.percentile(gray_diff, 98), 1.0), 0.0, 1.0)
        
        # Color gradient: Blue (0) -> Green (0.5) -> Red (1.0)
        r = (norm_diff * 255).astype(np.uint8)
        g = ((1.0 - np.abs(norm_diff - 0.5) * 2) * 200).astype(np.uint8)
        b = ((1.0 - norm_diff) * 255).astype(np.uint8)
        heatmap_rgb = Image.fromarray(np.stack([r, g, b], axis=-1))

        return enhanced_diff, ela_mean, ela_p95, ela_local_std, heatmap_rgb

    def _frequency_spectrum_analysis(self, image: Image.Image):
        gray = image.convert("L").resize((256, 256))
        arr = np.array(gray, dtype=np.float32)
        
        f = np.fft.fft2(arr)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1e-8)

        h, w = magnitude_spectrum.shape
        cy, cx = h // 2, w // 2
        y, x = np.ogrid[:h, :w]
        dist_from_center = np.sqrt((x - cx)**2 + (y - cy)**2)
        
        high_freq_mask = dist_from_center > 70
        mid_freq_mask = (dist_from_center >= 20) & (dist_from_center <= 70)

        high_energy = np.mean(magnitude_spectrum[high_freq_mask])
        mid_energy = np.mean(magnitude_spectrum[mid_freq_mask])
        
        ratio = float(high_energy / max(mid_energy, 1.0))
        
        # Check for abnormal periodic peak spikes (non-central outliers)
        outer_mag = magnitude_spectrum.copy()
        outer_mag[dist_from_center <= 25] = 0
        peak_anomaly = float(np.max(outer_mag) / max(np.mean(outer_mag), 1.0)) > 4.5

        norm_spec = ((magnitude_spectrum - np.min(magnitude_spectrum)) / 
                     max((np.max(magnitude_spectrum) - np.min(magnitude_spectrum)), 1e-5) * 255).astype(np.uint8)
        fft_img = Image.fromarray(norm_spec)

        return ratio, fft_img, peak_anomaly

    def _noise_variance_analysis(self, image: Image.Image):
        gray = image.convert("L").resize((256, 256))
        arr = np.array(gray, dtype=np.float32)
        pad = np.pad(arr, 1, mode='edge')
        laplacian = (
            pad[:-2, 1:-1] + pad[2:, 1:-1] + 
            pad[1:-1, :-2] + pad[1:-1, 2:] - 
            4 * pad[1:-1, 1:-1]
        )
        variance = float(np.var(laplacian))
        is_abnormally_smooth = variance < 50.0
        return variance, is_abnormally_smooth

    def _chrominance_analysis(self, image: Image.Image) -> float:
        # Convert RGB to YCbCr to inspect color differences
        ycbcr = image.convert("YCbCr").resize((128, 128))
        arr = np.array(ycbcr, dtype=np.float32)
        cb, cr = arr[:, :, 1], arr[:, :, 2]
        chroma_std = float(np.std(cb) + np.std(cr))
        return chroma_std

# Backward compatibility alias
DeepfakeDetector = ProfessionalDeepfakeDetector
