<template>
  <div class="config-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>系统配置管理</span>
          <el-button type="primary" @click="saveAllConfig">保存全部设置</el-button>
        </div>
      </template>

      <el-form label-width="150px" v-loading="loading">
        <!-- Assuming flat list for now, ideally it's categorized by tabs -->
        <el-row :gutter="20">
          <el-col :span="12" v-for="item in configList" :key="item.id">
            <el-form-item :label="item.info || item.menuName">
              <el-input 
                v-if="item.inputType === 'input'" 
                v-model="item.value" 
                :placeholder="item.desc" 
              />
              <el-switch 
                v-else-if="item.inputType === 'radio' && item.parameter" 
                v-model="item.value" 
                active-value="1" 
                inactive-value="0" 
              />
              <!-- Add other input types here (textarea, upload, etc) based on item.inputType -->
              <el-input 
                v-else 
                v-model="item.value" 
                :placeholder="item.desc" 
              />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const configList = ref([])
const loading = ref(false)

const fetchConfigs = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/system/config/list')
    if (res.data.code === 200) {
      configList.value = res.data.data
    }
  } catch (error) {
    ElMessage.error('获取配置失败')
  } finally {
    loading.value = false
  }
}

const saveAllConfig = async () => {
  loading.value = true
  try {
    // Transform list to Map
    const configMap = {}
    configList.value.forEach(item => {
      configMap[item.menuName] = item.value
    })
    const res = await axios.post('/api/admin/system/config/saveValues', configMap)
    if (res.data.code === 200) {
      ElMessage.success('保存成功')
    }
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchConfigs()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
