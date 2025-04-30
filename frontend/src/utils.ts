export function parseFilePath(s3Path : string){
    const parts = s3Path.split('*');
    const schoolName = parts[0];
    return(schoolName.split('_').join(' '));
}