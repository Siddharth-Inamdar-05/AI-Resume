import { FileSearch, Sparkles } from 'lucide-react';

const Header = () => {
  return (
    <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-primary/20 text-primary">
            <FileSearch className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-foreground flex items-center gap-2">
              AI Resume Screening & Skill Matching Engine
              <Sparkles className="w-4 h-4 text-primary" />
            </h1>
            <p className="text-sm text-muted-foreground">
              Upload resumes + paste JD to rank candidates
            </p>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
