const AiReportBlock = ({ report }) => {
    return (
        <div className="post-card">
            <div className="ai-report-wrapper">
                <strong className="ai-report-title">
                    Краткий отчет.
                </strong>
                <div className="ai-post__content">
                    {report}
                </div>
                <div className="ai-icon">
                    <p>*</p>
                </div>
            </div>
        </div>
    )
}

export default AiReportBlock;
