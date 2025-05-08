<template>
  <div ref="editorContainer" class="jetbrains-editor"></div>
</template>

<script>
import { basicSetup } from 'codemirror'
import { EditorView } from '@codemirror/view'
import { EditorState } from '@codemirror/state'
import { python } from '@codemirror/lang-python'

export default {
  name: 'PythonEditor',
  props: {
    modelValue: {
      type: String,
      default: ''
    },
    height: {
      type: String,
      default: '500px'
    }
  },
  emits: ['update:modelValue'],
  data() {
    return {
      editor: null,
      state: null
    }
  },
  mounted() {
    this.initializeEditor()
  },
  beforeUnmount() {
    if (this.editor) {
      this.editor.destroy()
    }
  },
  methods: {
    initializeEditor() {
      const extensions = [
        basicSetup,
        python(),
        EditorView.lineWrapping,
        EditorView.updateListener.of((update) => {
          if (update.docChanged) {
            this.$emit('update:modelValue', update.state.doc.toString())
          }
        })
      ]

      this.state = EditorState.create({
        doc: this.modelValue,
        extensions
      })

      this.editor = new EditorView({
        state: this.state,
        parent: this.$refs.editorContainer
      })
    }
  },
  watch: {
    modelValue(newVal) {
      if (newVal !== this.editor.state.doc.toString()) {
        this.editor.dispatch({
          changes: {
            from: 0,
            to: this.editor.state.doc.length,
            insert: newVal
          }
        })
      }
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

.jetbrains-editor .cm-editor {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.6;
}

.jetbrains-editor .cm-content {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.6;
}

.jetbrains-editor .cm-gutters {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
}

.jetbrains-editor .cm-cursor {
  border-left-color: #ffcc00;
}

.jetbrains-editor .cm-selectionBackground {
  background: rgba(100, 255, 100, 0.2);
}

.editor-container {
  height: 100%;
  overflow: hidden;
  border: 1px solid #444;
  border-radius: 4px;
}

.cm-editor {
  height: 100%;
}

.cm-scroller {
  overflow: auto;
}
</style>
