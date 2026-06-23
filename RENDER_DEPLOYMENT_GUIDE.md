# Render Deployment Guide

## Prerequisites
- Render account (free tier available)
- Git repository with the project code
- GitHub account (for connecting to Render)

## Step 1: Prepare Your Repository

### Ensure All Files Are Committed
```bash
git add .
git commit -m "Fix sklearn version compatibility and deployment issues"
git push origin main
```

### Verify Required Files
Your repository must include:
- `app.py` - Flask application
- `requirements.txt` - Python dependencies
- `Procfile` - Process configuration
- `runtime.txt` - Python version specification
- `render.yaml` - Render service configuration
- `train.py` - Training script
- `src/` - Source code directory
- `Notebook_Experiments/Data/heart.csv` - Training data
- `templates/` - HTML templates
- `static/` - Static files

## Step 2: Deploy via Render Dashboard

### Option A: Using render.yaml (Recommended)
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Review and click "Create Web Service"

### Option B: Manual Configuration
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the following:

**Build & Deploy Settings:**
- **Name**: heart-disease-prediction (or your preferred name)
- **Region**: Choose nearest region
- **Branch**: main
- **Runtime**: Python
- **Build Command**: `pip install -r requirements.txt && python train.py`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`

**Environment Variables:**
- `FLASK_SECRET_KEY`: Generate a random key (Render can auto-generate)
- `PYTHON_VERSION`: 3.10.11

5. Click "Create Web Service"

## Step 3: Monitor Deployment

Render will:
1. Clone your repository
2. Install dependencies from `requirements.txt`
3. Run `train.py` to generate model artifacts
4. Start the Flask application with Gunicorn
5. Provide a public URL

Monitor the deployment logs in the Render Dashboard to ensure:
- Dependencies install successfully
- Training completes without errors
- Application starts correctly

## Step 4: Access Your Application

Once deployment is successful, Render will provide:
- **Public URL**: `https://your-app-name.onrender.com`
- **SSL/TLS**: Automatically enabled
- **Auto-scaling**: Free tier includes basic scaling

## Step 5: Verify Deployment

Test the deployed application:
1. Open the provided URL in your browser
2. Submit a prediction form
3. Check the dashboard for model metrics
4. Verify prediction history works

## Troubleshooting Render Deployment

### Build Fails During Training
**Issue**: Training script fails during build
**Solution**: 
- Check logs in Render Dashboard
- Ensure `heart.csv` exists in `Notebook_Experiments/Data/`
- Verify all dependencies are in `requirements.txt`

### SimpleImputer _fill_dtype Error
**Issue**: Incompatible pickle files
**Solution**: This should be fixed with the updated code. If it persists:
- The build automatically retrains with compatible sklearn version
- Old artifacts are not committed to git

### Port Binding Issues
**Issue**: Application fails to bind to port
**Solution**: Ensure `app.py` uses `os.environ.get("PORT", 8080)` (already implemented)

### Memory Issues During Training
**Issue**: Build runs out of memory
**Solution**: 
- Free tier has limited memory (512MB)
- Consider pre-training locally and committing artifacts
- Or upgrade to a paid instance type

### Module Not Found Errors
**Issue**: Dependencies not installed
**Solution**: 
- Verify `requirements.txt` is correct
- Check that `-e .` is included for local package installation
- Review build logs for specific missing packages

## Alternative: Pre-Commit Artifacts (Faster Deployment)

To speed up deployments, you can pre-train locally and commit artifacts:

```bash
# Train locally
python train.py

# Commit artifacts (add to git)
git add Artifacts/
git commit -m "Add trained model artifacts"
git push origin main
```

Then update `render.yaml` build command:
```yaml
buildCommand: pip install -r requirements.txt
```

**Note**: This is faster but requires re-committing artifacts when models change.

## render.yaml Configuration

Your current `render.yaml`:
```yaml
services:
  - type: web
    name: heart-disease-prediction
    env: python
    buildCommand: pip install -r requirements.txt && python train.py
    startCommand: gunicorn --bind 0.0.0.0:$PORT app:app
    envVars:
      - key: FLASK_SECRET_KEY
        generateValue: true
      - key: PYTHON_VERSION
        value: 3.10.11
```

## Procfile

Your `Procfile`:
```
web: gunicorn --bind 0.0.0.0:$PORT app:app
```

## runtime.txt

Your `runtime.txt`:
```
python-3.10.11
```

## Deployment Checklist

- [ ] All files committed to git
- [ ] `requirements.txt` has correct sklearn version (1.3.0 - 1.6.0)
- [ ] `Procfile` exists and is valid
- [ ] `runtime.txt` specifies Python 3.10.11
- [ ] `render.yaml` is configured
- [ ] Training data exists in repository
- [ ] App uses PORT environment variable
- [ ] Database directory is created at runtime
- [ ] No hardcoded paths in code

## Post-Deployment Maintenance

### Updating the Model
1. Retrain locally: `python train.py`
2. Commit new artifacts: `git add Artifacts/ && git commit -m "Update model"`
3. Push: `git push origin main`
4. Render auto-deploys on push

### Monitoring
- Check Render Dashboard for logs
- Monitor resource usage
- Set up alerts for downtime

### Scaling
- Free tier: 512MB RAM, basic CPU
- Paid tiers: More resources, dedicated instances
- Consider upgrading for high traffic

## Security Notes

- `FLASK_SECRET_KEY` is auto-generated by Render
- Never commit secrets to git
- Use environment variables for sensitive data
- SSL/TLS is automatically enabled by Render

## Cost Estimate

- **Free Tier**: $0/month (limited resources, sleeps after inactivity)
- **Starter**: $7/month (512MB RAM, no sleep)
- **Standard**: $25/month (2GB RAM, better performance)

## Support

For Render-specific issues:
- [Render Documentation](https://render.com/docs)
- [Render Community](https://community.render.com)
- Check deployment logs in Render Dashboard
