/** @jsx hyperdom.jsx */
const hyperdom = require('hyperdom')
const httpism = require('httpism')

class App {
  constructor() {
    this.name = ''
    this.sentences = [
      {
        sentence: 'Hi there. My name is <name>',
        hint: 'You can say whatever name you want to be honest',
        fileName: '1',
        data: [],
      },
      {
        sentence: 'First they came for the French, and I did not speak out. Because I was not a French.',
        hint: 'Yeah, ok. a bit heavy',
        fileName: '2',
        data: [],
      },
      {
        sentence: 'My favorite form of transport is <?>, because <?>',
        hint: "Come on now. It can't be that difficult",
        fileName: '3',
        data: [],
      },
      {
        sentence: "Then they came for Jeremy Clarkson, and I think I'm right in saying I applauded",
        hint: 'Thinking of shit to get you to say is actually quite hard.',
        fileName: '4',
        data: [],
      },
      {
        sentence: 'Paul is awesome',
        hint: 'This one is important. Make sure you sound like you mean it',
        fileName: '5',
        data: [],
      },
      {
        sentence: 'Something something something else',
        hint: "Ok, last one. Say whatever you want",
        fileName: '6',
        data: [],
      },
    ]

    this.activeSentence = 0
    this.recording = false
  }

  stopRecording() {
    this.recording = false
    if(this.context) {
      this.context.close()
    }
    if(this.activeSentence + 1 < this.sentences.length) {
      this.activeSentence = this.activeSentence + 1
    } else {
      console.log(this.sentences)
    }
  }

  recordVoice() {
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
        self.sentences[self.activeSentence].data = [].concat.apply(self.sentences[self.activeSentence].data, left)
      }
    }

    navigator.mediaDevices.getUserMedia({ audio: true, video: false })
     .then(handleSuccess)
  }

  sendTheData() {
    if(!this.dataSending) {
      if(this.name == '') {
        this.error = 'need your name first!'
        return
      }
      this.dataSending = true
      this.error = ''
      httpism.post('/voices', {
        sampleRate: this.sampleRate,
        name: this.name,
        sentences: this.sentences.map(s => {
          return {data: s.data, fileName: s.fileName}
        })
      })
      this.showThanks = true
    }
  }

  render() {
    return <div>
      { this.showThanks ?
        <div>Thanks</div> :
        <div>
          <h1>I need your voice</h1>
          <p>
            Now then. Gonna need some data to train this thing up. There are some sentences below.
            Hit the record button and say those sentences. When you're done, hit done.
          </p>
          { this.sentences.length > this.activeSentence + 1 ?
          <div>
            <p class="sentence">{this.sentences[this.activeSentence].sentence}</p>
            <div>
              {
                this.recording ?
                  <a class="button" onclick={() => this.stopRecording()}>Done</a> :
                  <a class="button" onclick={()=>this.recordVoice()}>Record</a>
              }
            </div>
            <div class="hint">{this.sentences[this.activeSentence].hint}</div>
          </div> :
          <div>
            Cool. We're done. Just need your name, and then you can send this stuff to me
            <div>
              <label for="name">Name</label>
              <input id="name" binding={[this, 'name']} />
            </div>
            <div>
              { this.error }
              <a onclick={() => this.sendTheData() }>Send the data</a>
            </div>
          </div>
        }
      </div>
        }
    </div>
  }
}

hyperdom.append(document.body, new App());
