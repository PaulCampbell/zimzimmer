/** @jsx hyperdom.jsx */
const hyperdom = require('hyperdom')
const httpism = require('httpism')

class App {
  constructor() {
    this.data = []
  }

  recordVoice() {
    this.data = []
    const self = this
    this.recording = true
    this.context = new AudioContext()
    this.sampleRate = this.context.sampleRate
    var handleSuccess = (stream) => {
      var source = this.context.createMediaStreamSource(stream)
      var processor = this.context.createScriptProcessor(1024, 1, 1)
      source.connect(processor)
      processor.connect(this.context.destination)

      processor.onaudioprocess = (e) => {
        const left = e.inputBuffer.getChannelData(0);
        self.data = [].concat.apply(self.data, left)
      }
    }

    navigator.mediaDevices.getUserMedia({ audio: true, video: false })
     .then(handleSuccess)
  }

  stopRecording() {
    this.recording = false
    if(this.context) {
      this.context.close()
    }
  }

  predict() {
    if(!this.dataSending) {
      this.dataSending = true
      this.error = ''
      return httpism.post('/predict', {
        sampleRate: this.sampleRate,
        data: this.data
      }).then((res) => {
        this.dataSending = false
        this.showThanks = true
        console.log(res)
      })
    }
  }


  render() {
    return <section class="section">
      <div class="container">
        <h1 class="title">Speak</h1>
        {
          this.recording ?
            <a class="button" onclick={() => this.stopRecording()}>Done</a> :
            <a class="button" onclick={()=>this.recordVoice()}>Start speaking</a>
        }
        {
          this.data ?
            <a class="button" onclick={() => this.predict()}>Send</a> : undefined }
      </div>
    </section>
  }
}

hyperdom.append(document.body, new App());
