from pathlib import Path
import json
import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from rag import ingest, retrieve, generate

ROOT=Path(__file__).parent
st.set_page_config(page_title='AAPL Intelligent System',page_icon='📈',layout='wide')
@st.cache_data
def load():
    return json.loads((ROOT/'data/research.json').read_text()),json.loads((ROOT/'data/corpus.json').read_text())
data,corpus=load()
st.markdown("""<style>
.stApp{background:#f5f8fd;color:#152b4b}
.block-container{padding-top:2rem;max-width:1500px}
[data-testid="stSidebar"]{background:#fff;border-right:1px solid #dce6f3}
h1,h2,h3{color:#102d55;letter-spacing:-.5px}
[data-testid="stMetric"]{background:white;border:1px solid #dce6f3;border-radius:14px;padding:18px}
[data-testid="stMetricLabel"]{color:#58708e}
[data-testid="stMetricValue"]{color:#174b96}
.hero{background:linear-gradient(115deg,#112f60 0%,#1857ac 65%,#357de0 100%);padding:32px 36px;border-radius:20px;color:white;margin:10px 0 24px}
.hero h2{color:white;font-size:32px;margin:8px 0}.hero p{color:#dceaff;max-width:760px;line-height:1.7}
.eyebrow{font-size:11px;letter-spacing:2px;font-weight:700;text-transform:uppercase}.pill{display:inline-block;background:#ffffff20;border:1px solid #ffffff38;border-radius:20px;padding:5px 12px;font-size:12px;margin:4px 7px 0 0}
.engine{background:white;border:1px solid #dce6f3;border-top:4px solid #2464cc;border-radius:15px;padding:24px;min-height:265px;margin-top:8px}
.engine.ai{border-top-color:#6395d9}.engine h3{font-size:23px;margin:10px 0}.engine p{color:#58708e;line-height:1.65}.tags{color:#245aa5;font-size:12px;line-height:2.1}
.note{border-left:3px solid #5b8ed6;background:#eaf2ff;padding:14px 18px;border-radius:0 9px 9px 0;color:#355578;font-size:13px;margin-top:20px}
.step{background:white;border:1px solid #dce6f3;border-radius:12px;padding:18px;min-height:130px}.step strong{display:block;color:#1f5fbf;margin-bottom:8px}.step span{font-size:13px;color:#58708e}
</style>""",unsafe_allow_html=True)
NAV={'🏠 Overview / Home':'Overview','📊 Model comparison':'Model comparison','📉 Forecast visualization':'Forecast chart','🌊 Volatility / GJR-GARCH':'GJR-GARCH risk','🧠 Explainable AI':'Explainable AI','📚 Financial report RAG':'Financial report RAG'}
st.sidebar.markdown('### 📈 AAPL\nIntelligent System')
st.sidebar.caption('QUANTITATIVE RESEARCH + AI KNOWLEDGE')
st.sidebar.divider()
selected=st.sidebar.radio('Workspace',list(NAV),key='nav')
page=NAV[selected]
st.sidebar.divider()
seed=st.sidebar.selectbox('Experiment seed',[42,123,2026])
st.sidebar.caption('RESEARCH DATASET')
st.sidebar.markdown('**AAPL · 2010–2026**')
st.sidebar.caption('04 Jan 2010 — 01 Oct 2026')
st.sidebar.info('Historical experiment\n\nSaved forecasts and explanations')
def navigate(label):
    st.session_state.nav=label
rows=pd.DataFrame(data['rows'][str(seed)])
metrics=pd.DataFrame(data['metrics']); metrics=metrics[metrics.seed==seed]
if page!='Overview':
    st.title(selected)
    st.caption('AAPL Intelligent System / Research workspace')

def line(frame,columns,ytitle='Price (USD)'):
    fig=go.Figure()
    for col in columns: fig.add_trace(go.Scatter(x=frame.date,y=frame[col],name=col,mode='lines+markers' if len(frame)==1 else 'lines'))
    fig.update_layout(height=430,margin=dict(l=10,r=10,t=20,b=10),yaxis_title=ytitle,legend=dict(orientation='h'),template='plotly_white')
    st.plotly_chart(fig,use_container_width=True)

def download(name):
    p=ROOT/'data'/name
    st.download_button('Download '+name,p.read_bytes(),file_name=name,key=name)

if page=='Overview':
    st.caption('WORKSPACE / OVERVIEW')
    st.title('AAPL Intelligent System')
    st.markdown('<div class="hero"><div class="eyebrow">Two engines. One research workspace.</div><h2>Explore forecasts.<br>Understand the evidence.</h2><p>Bring quantitative forecasting and financial knowledge together. Compare model performance, understand prediction drivers, and explore company reports with traceable sources.</p><span class="pill">Quantitative Engine</span><span class="pill">AI Knowledge Engine</span><span class="pill">AAPL · 2010–2026</span></div>',unsafe_allow_html=True)
    a,b,c,d=st.columns(4)
    a.metric('Dataset observations','4,212'); b.metric('Historical test days','629'); c.metric('Forecasting models','5'); d.metric('Experiment seeds','3')
    st.caption('Five price models: ARIMA, BiLSTM, Transformer, Ridge and XGBoost. GJR-GARCH provides volatility estimates; additional baselines support comparison.')
    st.subheader('Your research engines')
    left,right=st.columns(2,gap='large')
    with left:
        st.markdown('<div class="engine"><div class="eyebrow">01 / Quantitative Engine</div><h3>📊 Forecast & evaluate</h3><p>Study price forecasts and market volatility through the hybrid model architecture. Compare errors and directional performance across repeated experiments.</p><div class="tags">ARIMA · BiLSTM · Transformer<br>GJR-GARCH · Ridge · XGBoost<br>Model comparison · Forecasts · Volatility · XAI</div></div>',unsafe_allow_html=True)
        st.button('Explore model performance →',on_click=navigate,args=('📊 Model comparison',),use_container_width=True,type='primary')
    with right:
        st.markdown('<div class="engine ai"><div class="eyebrow">02 / AI Knowledge Engine</div><h3>📚 Retrieve & understand</h3><p>Explore research evidence and uploaded financial reports. Retrieve relevant passages with source references and optionally generate grounded answers.</p><div class="tags">PDF reports · Research documents<br>Source citations · Availability-date filtering<br>Document retrieval · Optional LLM answers</div></div>',unsafe_allow_html=True)
        st.button('Open financial report RAG →',on_click=navigate,args=('📚 Financial report RAG',),use_container_width=True)
    st.markdown('')
    left,right=st.columns([1.65,1],gap='large')
    with left:
        st.subheader('AAPL price overview')
        st.caption('Saved test period · 01 Apr 2024 — 01 Oct 2026 · USD')
        fig=go.Figure(go.Scatter(x=rows.date,y=rows.actual,name='Actual close',line=dict(color='#2764cc',width=2),fill='tozeroy',fillcolor='rgba(39,100,204,0.07)'))
        fig.update_layout(height=300,margin=dict(l=10,r=10,t=10,b=10),paper_bgcolor='white',plot_bgcolor='white',yaxis_title='Price (USD)',xaxis=dict(showgrid=False),yaxis=dict(gridcolor='#edf2fa'),hovermode='x unified')
        st.plotly_chart(fig,use_container_width=True)
        st.button('View forecast visualization →',on_click=navigate,args=('📉 Forecast visualization',))
    with right:
        st.subheader('Research snapshot')
        st.caption(f'Selected experiment · seed {seed}')
        table=metrics.set_index('model').loc[['ARIMA','BiLSTM','Transformer','Ridge','XGBoost','WeightedAvg','MajorityDirection'],['DA']].rename(columns={'DA':'Direction accuracy (%)'})
        st.dataframe(table.style.format('{:.2f}'),use_container_width=True,height=320)
        st.caption('WeightedAvg and MajorityDirection are comparison baselines. High price-fit R² does not imply high direction accuracy.')
        st.markdown('**GJR-GARCH · Volatility model**')
        st.caption('Evaluated separately using variance metrics; direction accuracy is not applicable.')
        st.button('View GJR-GARCH results →',on_click=navigate,args=('🌊 Volatility / GJR-GARCH',))
        st.button('Understand model predictions →',on_click=navigate,args=('🧠 Explainable AI',))
    st.subheader('How the system works')
    for col,title,description in zip(st.columns(3),['01 · Explore the data','02 · Evaluate & explain','03 · Retrieve evidence'],['Inspect the historical AAPL dataset and saved forecast period.','Compare price and direction metrics, volatility, and model contributions.','Search financial documents and inspect cited passages supporting answers.']):
        with col: st.markdown(f'<div class="step"><strong>{title}</strong><span>{description}</span></div>',unsafe_allow_html=True)
    st.markdown('<div class="note"><b>Research context.</b> This workspace displays saved experimental outputs, not live predictions. Ensemble improvement has not been established, and the test era was previously inspected. Report retrieval is available; generated answers require an API configuration.</div>',unsafe_allow_html=True)
    st.subheader('System architecture')
    st.caption('Two connected research engines · historical experiment workflow')
    st.graphviz_chart("""digraph architecture {
        graph [rankdir=TB, bgcolor="transparent"];
        node [shape=box, style="rounded,filled", fillcolor="#eaf2ff", color="#2464cc", fontname="Arial"];
        subgraph cluster_quant { label="Quantitative Engine"; color="#2464cc";
          prices [label="Historical AAPL data / features"];
          base [label="ARIMA / BiLSTM / Transformer"];
          vol [label="GJR-GARCH volatility"];
          meta [label="OOF forecasts + volatility + indicators"];
          stack [label="Ridge / XGBoost"];
          prices -> base; prices -> vol; base -> meta; vol -> meta; meta -> stack;
        }
        subgraph cluster_ai { label="AI Knowledge Engine"; color="#6395d9";
          docs [label="Financial reports / research evidence"];
          retrieval [label="Text extraction / passage retrieval"];
          answer [label="Cited evidence / optional LLM answer"];
          docs -> retrieval -> answer;
        }
        dashboard [label="Dashboard: forecasts / evaluation / explanations / evidence", fillcolor="#cfe2ff"];
        base -> dashboard; stack -> dashboard; vol -> dashboard; answer -> dashboard;
    }""", use_container_width=True)
    st.caption('Model training is offline. This app displays saved outputs; uploaded reports are retrieved in session.')
    with st.expander('Dataset, architecture & reproducibility'):
        st.write('Historical features → ARIMA, BiLSTM and Transformer forecasts + GJR-GARCH volatility and indicators → out-of-fold meta-feature matrix → Ridge / XGBoost.')
        st.write('Raw coverage: 2010-01-04 to 2026-10-01. All 11 supplied audit checks passed; this does not prove the absence of every possible leakage issue.')
        st.json({'base_models':data['parameters'],'meta_models':data['metaParameters']})
elif page=='Model comparison':
    st.write('MAE and RMSE are in USD; MAPE and direction accuracy (DA) are percentages. R² measures price fit, not direction skill.')
    st.dataframe(metrics[['model','n','MAE','RMSE','MAPE','R2','DA','BalancedAccuracy','MacroF1']],hide_index=True,use_container_width=True)
    ci=pd.DataFrame(data['ci']); st.subheader('Direction accuracy · 95% block-bootstrap intervals')
    st.dataframe(ci[ci.seed==seed],hide_index=True)
    st.caption('Repeated seeds describe training variability. Block-bootstrap intervals account for local temporal dependence; they are not per-forecast confidence probabilities.')
    for name in ['test_metrics_by_seed.csv','direction_accuracy_CI.csv','paired_DA_family_adjusted.csv','tuning_trials.csv']: download(name)
elif page=='Forecast chart':
    chosen=st.multiselect('Models',[c for c in rows if c not in ['date','actual','previous']],default=['Ridge','Transformer','ARIMA'])
    dates=rows.date.tolist(); start,end=st.select_slider('Historical period',options=dates,value=(dates[0],dates[-1]))
    selected=rows[(rows.date>=start)&(rows.date<=end)]
    line(selected,['actual']+chosen)
    st.dataframe(selected[['date','actual','previous']+chosen],hide_index=True,use_container_width=True)
    download('test_predictions.csv')
elif page=='GJR-GARCH risk':
    vol=pd.DataFrame(data['volatility']); vol['Forecast sigma (%)']=vol.forecast_variance.clip(lower=0)**.5
    st.write('GJR-GARCH models conditional volatility. It does not directly predict price direction.')
    line(vol,['Forecast sigma (%)'],'Conditional volatility (%)')
    st.dataframe(pd.DataFrame(data['volMetrics']),hide_index=True)
    st.caption('QLIKE and variance MSE compare variance forecasts with a squared-innovation proxy. Lower values are better. This is not a calibrated price prediction interval.')
elif page=='Explainable AI':
    st.write('Inspect every model using the explanation evidence available in the saved experiment.')
    model=st.selectbox('Explain model',['ARIMA','BiLSTM','Transformer','Ridge','XGBoost','GJR-GARCH','WeightedAvg','MajorityDirection'],index=3)
    day=st.selectbox('Forecast date',rows.date.tolist())
    idx=rows.index[rows.date==day][0]; exp=data['explanations'][str(seed)]
    methods={
        'ARIMA':'Uses past observations and forecast errors through its fitted ARIMA structure. The saved order and forecast diagnostics are available; fitted component contributions are not exported.',
        'BiLSTM':'Processes a 60-observation sequence in both directions within that historical window. Input attribution requires the trained network, preprocessing and input windows, which are not exported here.',
        'Transformer':'Uses attention to combine information within a historical input window. Attention weights alone are not feature importance. Integrated gradients or controlled perturbations require model weights and inputs.',
        'GJR-GARCH':'Models conditional variance with asymmetric responses to shocks. Parameter and shock decompositions require fitted coefficients and residual history; this export contains variance forecasts.',
        'WeightedAvg':'Combines base forecasts. Exact contributions require the fitted ensemble weights, which are not included in the explanation export.',
        'MajorityDirection':'Direction baseline. Its output is evaluated against realized direction; this is not a calibrated probability.'}
    if model in ['Ridge','XGBoost']:
        base=exp['ridgeBase'] if model=='Ridge' else exp['xgbBase'][idx]
        contributions=exp['ridge' if model=='Ridge' else 'xgb'][idx]
        a,b,c=st.columns(3); a.metric('Baseline (USD)',f'{base:.4f}'); b.metric('Forecast (USD)',f'{rows.iloc[idx][model]:.4f}'); c.metric('Actual (USD)',f'{rows.iloc[idx].actual:.4f}')
        fig=go.Figure(go.Waterfall(x=['Baseline']+data['features']+['Forecast'],measure=['absolute']+['relative']*len(contributions)+['total'],y=[base]+contributions+[0],connector={'line':{'color':'#bbb'}}))
        fig.update_layout(height=440,yaxis_title='Price contribution (USD)',template='plotly_white')
        st.plotly_chart(fig,use_container_width=True)
        ranked=sorted(zip(data['features'],contributions),key=lambda item:abs(item[1]),reverse=True)
        st.subheader('What moved this forecast?')
        st.write(f"The reference forecast is ${base:.2f}. Feature contributions change it by ${sum(contributions):+.2f}, giving ${float(rows.iloc[idx][model]):.2f}.")
        for name,value in ranked[:3]:
            st.write(f"• {name}: {'raises' if value>=0 else 'lowers'} the forecast by ${abs(value):.2f} relative to the explanation reference.")
        st.caption('Base-model feature names describe their forecast inputs to the ensemble. This is not an explanation of the internal neural network.')
        view=st.radio('Contribution view',['Selected forecast','Across saved test period'],horizontal=True)
        if view=='Selected forecast':
            importance=pd.DataFrame(ranked,columns=['Feature','Contribution (USD)'])
            fig=go.Figure(go.Bar(x=importance['Contribution (USD)'],y=importance.Feature,orientation='h',marker_color=['#2464cc' if v>=0 else '#dc6060' for v in importance['Contribution (USD)']]))
            fig.update_layout(xaxis_title='Signed contribution (USD)',yaxis=dict(autorange='reversed'),height=350,template='plotly_white')
        else:
            values=pd.DataFrame(exp['ridge' if model=='Ridge' else 'xgb'],columns=data['features']).abs().mean().sort_values()
            fig=go.Figure(go.Bar(x=values.values,y=values.index,orientation='h',marker_color='#2464cc'))
            fig.update_layout(xaxis_title='Mean absolute contribution (USD)',height=350,template='plotly_white')
            st.caption('Descriptive importance across the saved test period, not out-of-sample evidence of causality or predictive skill.')
        st.plotly_chart(fig,use_container_width=True)
        st.dataframe(pd.DataFrame({'Feature':data['features'],'Input':[exp['features'][idx][f] for f in data['features']],'Contribution (USD)':contributions}),hide_index=True)
        st.caption('Ridge: exact linear contributions relative to mean scaled training inputs. XGBoost: native TreeSHAP. These explain the meta-model, not causality or the internal neural models.')
        st.write(f'Reconstruction residual: {float(rows.iloc[idx][model])-base-sum(contributions):.8f} USD')
    elif model=='GJR-GARCH':
        st.info(methods[model])
        v=pd.DataFrame(data['volatility']); selected_vol=v[v.date==day]
        if selected_vol.empty: st.warning('No volatility output for this date.')
        else:
            value=selected_vol.iloc[0]
            st.metric('Forecast volatility (%)',f"{max(value.forecast_variance,0)**.5:.4f}")
            st.dataframe(selected_vol,hide_index=True)
        st.caption('Volatility diagnostic, not feature attribution or a directional forecast.')
    else:
        st.info(methods[model])
        r=rows.iloc[idx]; prediction=float(r[model]); previous=float(r.previous)
        a,b,c=st.columns(3)
        a.metric('Saved forecast (USD)',f'{prediction:.4f}')
        b.metric('Change from previous close (USD)',f'{prediction-previous:+.4f}')
        c.metric('Forecast minus actual (USD)',f'{prediction-float(r.actual):+.4f}')
        st.caption('Observed forecast behavior; these diagnostics do not attribute predictions to input features.')
        st.subheader('Selected forecast explained')
        delta=prediction-previous
        direction='higher' if delta>0 else 'lower' if delta<0 else 'unchanged'
        pct=100*delta/previous if previous else 0
        st.write(f"On {day}, {model} forecast ${prediction:.2f}, {direction} relative to the previous close of ${previous:.2f} ({pct:+.2f}%). The observed close was ${float(r.actual):.2f}; absolute forecast error was ${abs(prediction-float(r.actual)):.2f}.")
        fig=go.Figure(go.Bar(x=['Previous close','Model forecast','Actual close'],y=[previous,prediction,float(r.actual)],marker_color=['#94b9ee','#2464cc','#18395f'],text=[f'${x:.2f}' for x in [previous,prediction,float(r.actual)]],textposition='outside'))
        fig.update_layout(height=330,yaxis_title='Price (USD)',template='plotly_white',margin=dict(t=35,b=20),yaxis=dict(rangemode='tozero'))
        st.plotly_chart(fig,use_container_width=True)
        st.subheader('Forecast history through selected date')
        if idx==0:
            st.info('This is the first saved test date. Select a later date to display a historical trend. The comparison above shows all three values for this date.')
        else:
            line(rows.iloc[max(0,idx-29):idx+1],['actual','previous',model])
        if model=='ARIMA':
            p_order,d_order,q_order=data['parameters']['ARIMA']['order']
            st.write(f'ARIMA({p_order}, {d_order}, {q_order}) uses differencing and moving-average forecast error terms. Fitted error terms are needed to decompose this particular forecast.')
        if model in data['parameters']:
            with st.expander('Model settings · not feature importance'):
                st.dataframe(pd.DataFrame([{'Setting':k,'Value':str(v)} for k,v in data['parameters'][model].items()]),hide_index=True,use_container_width=True)
        if model in ['ARIMA','BiLSTM','Transformer']:
            st.warning('Feature attribution is not yet integrated for this model. This view provides forecast diagnostics only; it should not be reported as a completed XAI method.')
    st.subheader('Explanation coverage')
    st.dataframe(pd.DataFrame([
        {'Model':m,'Available explanation':('Exact linear contributions' if m=='Ridge' else 'TreeSHAP contributions' if m=='XGBoost' else 'Conditional volatility diagnostics' if m=='GJR-GARCH' else 'Forecast diagnostics and method description')}
        for m in ['ARIMA','BiLSTM','Transformer','Ridge','XGBoost','GJR-GARCH','WeightedAvg','MajorityDirection']
    ]),hide_index=True,use_container_width=True)

else:
    st.write('Search research evidence and uploaded financial reports. Answers retain source titles, page numbers and availability dates.')
    st.info('Built-in sources describe this experiment. No company annual report is included. Upload reports to ask report-specific questions.')
    if 'documents' not in st.session_state: st.session_state.documents=[]
    with st.expander('Add financial reports'):
        files=st.file_uploader('PDF, TXT or Markdown',type=['pdf','txt','md'],accept_multiple_files=True)
        available=st.date_input('Date the document became publicly available')
        st.caption('Used for the retrieval cutoff. Uploads stay in this session memory; a disconnected session may lose them.')
        if st.button('Index documents'):
            try:
                if not files: raise ValueError('Choose a report file before indexing.')
                new=[]
                for f in files or []: new.extend(ingest(f.name,f.getvalue(),available))
                if len(st.session_state.documents)+len(new)>5000: raise ValueError('Session limit: 5,000 passages. Clear documents first.')
                existing={(d['title'],d['page'],d['text'],d['availableAt']) for d in st.session_state.documents}
                unique=[d for d in new if (d['title'],d['page'],d['text'],d['availableAt']) not in existing]
                st.session_state.documents.extend(unique); st.session_state.pop('rag_result',None); st.success(f'Indexed {len(unique)} new passages.')
            except Exception as exc: st.error(str(exc))
        if st.button('Clear uploaded documents'):
            st.session_state.documents=[]
            st.session_state.pop('rag_result',None)
    st.caption(f"{len(st.session_state.documents)} uploaded passages · {len(corpus)} built-in research passages")
    scope=st.selectbox('Evidence scope',['Report','Research','All'],index=1)
    st.caption('Report searches only uploaded disclosures. Research searches saved experiment notes. All combines both.')
    historical=st.checkbox('Restrict evidence by availability date')
    cutoff=st.date_input('Available on or before') if historical else None
    suggestions=['Custom question',
        "What were Apple's total net sales and net income? Include fiscal year, currency, units and source pages.",
        "How did iPhone and Services revenue change compared with the previous year?",
        "What supply chain risks does Apple describe? Cite source pages.",
        "What was cash flow from operating activities? Include fiscal year and units.",
        "How much did Apple spend on research and development?",
        "What does the report say about Greater China net sales?",
        "What is the Ridge model direction accuracy?",
        "How do ARIMA, BiLSTM and Transformer perform in this experiment?"]
    def choose_question():
        st.session_state.pop('rag_result',None)
        st.session_state.rag_question='' if st.session_state.suggested_question=='Custom question' else st.session_state.suggested_question
    st.selectbox('Suggested question',suggestions,key='suggested_question',on_change=choose_question)
    question=st.text_input('Research question',placeholder='Ask a question in English',key='rag_question')
    st.caption('English answers. Report questions require an uploaded report; answers must include source citations.')
    def secret(name):
        if os.getenv(name): return os.getenv(name)
        try: return st.secrets.get(name,'')
        except Exception: return ''
    with st.expander('LLM connection settings'):
        st.caption('Optional. These fields remain in this session only. Do not share your API key in chat.')
        entered_key=st.text_input('OpenAI API key',type='password',key='llm_api_key')
        entered_model=st.text_input('Model ID',key='llm_model_id',placeholder='Enter a model ID available to your API account')
    key=entered_key.strip() or secret('OPENAI_API_KEY')
    model=entered_model.strip() or secret('OPENAI_MODEL')
    use_llm=st.checkbox('Generate an LLM answer from retrieved passages',disabled=not bool(key and model))
    st.info('LLM connection configured · not yet verified' if key and model else 'Evidence search mode: add an API key and model ID above to enable generated answers.')
    if use_llm: st.caption('Search sends your question and up to five retrieved passages to OpenAI. API charges may apply.')
    if st.button('Search evidence',type='primary'):
        st.session_state.pop('rag_result',None)
        report_question=st.session_state.suggested_question in suggestions[1:7] and question==st.session_state.suggested_question
        effective_scope='Report' if report_question else scope
        if not question.strip(): st.warning('Enter or select a question first.')
        elif effective_scope=='Report' and not st.session_state.documents:
            st.warning('Upload a financial report and click Index documents first. Built-in research notes cannot answer this report question.')
        else:
            evidence=retrieve(question,corpus+st.session_state.documents,cutoff,effective_scope)
            result={'question':question,'scope':effective_scope,'cutoff':str(cutoff) if cutoff else 'None','evidence':evidence,'answer':None,'error':None}
            if evidence and use_llm:
                try:
                    with st.spinner('Generating a grounded answer…'): result['answer']=generate(question,evidence,key,model)
                except Exception as exc:
                    result['error']=str(exc) if isinstance(exc,ValueError) else 'Connection failed. Check network access and API settings; retrieved evidence is available below.'
            st.session_state.rag_result=result
    result=st.session_state.get('rag_result')
    if result:
        st.subheader('Last submitted search')
        st.write(result['question'])
        st.caption(f"Sources: {result['scope']} · availability cutoff: {result['cutoff']}. Changes above apply when you search again.")
        if result['error']: st.error(result['error'])
        if not result['evidence']: st.warning('No matching evidence found. Check the report, source scope and date filter; try terms used in the document.')
        elif result['answer']:
            st.write(result['answer'])
            st.caption('Citation IDs are checked, but factual support requires reviewing the passages.')
        else: st.info('Source excerpts below are retrieved evidence, not an LLM-generated answer.')
        for i,doc in enumerate(result['evidence']):
            with st.expander(f"[S{i+1}] {doc['title']} · page {doc['page']} · available {doc['availableAt']}",expanded=True): st.write(doc['text'])
    st.caption('Keyword retrieval works best with English search terms for English source documents. Availability filtering prevents later documents entering historical retrieval; it does not validate forecasting accuracy.')
