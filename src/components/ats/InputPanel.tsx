import { useState, useRef } from 'react';
import { Upload, FileText, X, Loader2, Trash2, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { UploadedFile, LoadingStatus, LOADING_MESSAGES } from '@/types/candidate';

interface InputPanelProps {
  onEvaluate: (jdText: string, files: UploadedFile[]) => void;
  loadingStatus: LoadingStatus;
}

const MAX_JD_LENGTH = 10000;

const InputPanel = ({ onEvaluate, loadingStatus }: InputPanelProps) => {
  const [jdText, setJdText] = useState('');
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const isLoading = loadingStatus !== 'idle';
  const canEvaluate = jdText.trim().length > 0 && uploadedFiles.length > 0 && !isLoading;

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    const pdfFiles = files.filter(f => f.type === 'application/pdf');
    
    const newFiles: UploadedFile[] = pdfFiles.map(file => ({
      id: crypto.randomUUID(),
      file,
      name: file.name,
      size: file.size,
    }));

    setUploadedFiles(prev => [...prev, ...newFiles]);
    
    // Reset input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const removeFile = (id: string) => {
    setUploadedFiles(prev => prev.filter(f => f.id !== id));
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const handleClear = () => {
    setJdText('');
    setUploadedFiles([]);
  };

  const handleEvaluate = () => {
    if (canEvaluate) {
      onEvaluate(jdText, uploadedFiles);
    }
  };

  return (
    <div className="panel h-full flex flex-col">
      <div className="panel-header rounded-t-xl">
        <h2 className="text-lg font-semibold text-foreground">Input Configuration</h2>
        <p className="text-sm text-muted-foreground mt-1">Configure job requirements and upload candidate resumes</p>
      </div>

      <div className="flex-1 p-6 space-y-6 overflow-auto scrollbar-thin">
        {/* Job Description */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <label className="text-sm font-medium text-foreground">
              Job Description
            </label>
            <span className={`text-xs ${jdText.length > MAX_JD_LENGTH * 0.9 ? 'text-destructive' : 'text-muted-foreground'}`}>
              {jdText.length.toLocaleString()} / {MAX_JD_LENGTH.toLocaleString()}
            </span>
          </div>
          <Textarea
            placeholder="Paste job description here..."
            value={jdText}
            onChange={(e) => setJdText(e.target.value.slice(0, MAX_JD_LENGTH))}
            disabled={isLoading}
            className="min-h-[200px] resize-none bg-input border-border focus:border-primary focus:ring-primary/20 text-foreground placeholder:text-muted-foreground"
          />
        </div>

        {/* Resume Upload */}
        <div className="space-y-3">
          <label className="text-sm font-medium text-foreground">
            Upload Resumes (PDF)
          </label>
          
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            multiple
            onChange={handleFileChange}
            disabled={isLoading}
            className="hidden"
          />

          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={isLoading}
            className="w-full border-2 border-dashed border-border rounded-xl p-8 hover:border-primary/50 hover:bg-primary/5 transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
          >
            <div className="flex flex-col items-center gap-3 text-muted-foreground group-hover:text-primary transition-colors">
              <Upload className="w-8 h-8" />
              <div className="text-center">
                <p className="font-medium">Click to upload or drag files</p>
                <p className="text-xs mt-1">PDF files only</p>
              </div>
            </div>
          </button>

          {/* File List */}
          {uploadedFiles.length > 0 && (
            <div className="space-y-2 max-h-[200px] overflow-auto scrollbar-thin">
              {uploadedFiles.map((file) => (
                <div key={file.id} className="file-item">
                  <div className="flex items-center gap-3">
                    <FileText className="w-4 h-4 text-primary" />
                    <div>
                      <p className="text-sm font-medium text-foreground truncate max-w-[200px]">
                        {file.name}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {formatFileSize(file.size)}
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => removeFile(file.id)}
                    disabled={isLoading}
                    className="p-1.5 rounded-lg hover:bg-destructive/20 text-muted-foreground hover:text-destructive transition-colors disabled:opacity-50"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          )}

          {uploadedFiles.length > 0 && (
            <p className="text-xs text-muted-foreground">
              {uploadedFiles.length} file{uploadedFiles.length !== 1 ? 's' : ''} selected
            </p>
          )}
        </div>

        {/* Loading Status */}
        {isLoading && (
          <div className="flex items-center gap-3 p-4 bg-primary/10 rounded-xl border border-primary/20">
            <Loader2 className="w-5 h-5 text-primary animate-spin" />
            <span className="text-sm font-medium text-primary">
              {LOADING_MESSAGES[loadingStatus]}
            </span>
          </div>
        )}

        {/* Validation Warning */}
        {!canEvaluate && !isLoading && (
          <div className="flex items-start gap-2 p-3 bg-muted/50 rounded-lg border border-border">
            <AlertCircle className="w-4 h-4 text-muted-foreground mt-0.5 shrink-0" />
            <p className="text-xs text-muted-foreground">
              {!jdText.trim() && 'Enter a job description'}
              {jdText.trim() && uploadedFiles.length === 0 && 'Upload at least one resume'}
            </p>
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="p-6 pt-0 space-y-3">
        <Button
          onClick={handleEvaluate}
          disabled={!canEvaluate}
          className="w-full h-12 text-base font-semibold bg-primary hover:bg-primary/90 text-primary-foreground disabled:opacity-50"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              Processing...
            </>
          ) : (
            'Evaluate Candidates'
          )}
        </Button>
        <Button
          variant="outline"
          onClick={handleClear}
          disabled={isLoading || (jdText.length === 0 && uploadedFiles.length === 0)}
          className="w-full h-10 border-border hover:bg-secondary text-muted-foreground hover:text-foreground"
        >
          <Trash2 className="w-4 h-4 mr-2" />
          Clear All
        </Button>
      </div>
    </div>
  );
};

export default InputPanel;
