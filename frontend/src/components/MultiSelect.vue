<template>
  <div class="multiselect-wrapper">
    <div class="selected-countries" @click="toggleDropdown">
      <span v-if="selectedCountries.length === 0">Выберите страны</span>
      <span v-else>
        {{ selectedCountries.map(country => country.name).join(', ') }}
      </span>
      <span class="arrow">{{ isOpen ? '▲' : '▼' }}</span>
    </div>

    <div v-if="isOpen" class="dropdown">
      <div class="search" v-if="enableSearch">
        <input type="text" v-model="searchQuery" placeholder="Поиск..." @input="filterOptions">
      </div>
      <div class="options">
        <div v-for="country in filteredCountries" :key="country.id" class="option">
          <label>
            <input 
              type="checkbox" 
              :value="country" 
              v-model="selectedCountries"
              @change="updateSelected"
            >
            {{ country.name }}
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    options: {
      type: Array,
      required: true
    },
    value: {
      type: Array,
      default: () => []
    },
    enableSearch: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      selectedCountries: [...this.value],
      isOpen: false,
      searchQuery: '',
      filteredCountries: [...this.options]
    }
  },
  watch: {
    value(newVal) {
      this.selectedCountries = [...newVal];
      console.log(newVal);
    }
  },
  methods: {
    toggleDropdown() {
      this.isOpen = !this.isOpen;
      if (this.isOpen) {
        this.filterOptions();
      }
    },
    filterOptions() {
      if (!this.searchQuery) {
        this.filteredCountries = [...this.options];
        return;
      }
      const query = this.searchQuery.toLowerCase();
      this.filteredCountries = this.options.filter(country => 
        country.name.toLowerCase().includes(query)
      );
    },
    updateSelected() {
      this.$emit('update:modelValue', [...this.selectedCountries]);
    },
    closeOnClickOutside(e) {
      if (!this.$el.contains(e.target)) {
        this.isOpen = false;
      }
    }
  },
  mounted() {
    document.addEventListener('click', this.closeOnClickOutside);
  },
  beforeDestroy() {
    document.removeEventListener('click', this.closeOnClickOutside);
  }
}
</script>

<style scoped>
.multiselect-wrapper {
  position: relative;
  width: 100%;
  max-width: 400px;
  font-family: Arial, sans-serif;
}

.selected-countries {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  background-color: white;
}

.arrow {
  margin-left: 10px;
}

.dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: white;
  z-index: 1000;
  margin-top: 5px;
  max-height: 300px;
  overflow-y: auto;
}

.search {
  padding: 8px;
  border-bottom: 1px solid #eee;
}

.search input {
  width: 100%;
  padding: 5px;
  box-sizing: border-box;
}

.options {
  padding: 5px 0;
}

.option {
  padding: 8px 15px;
}

.option:hover {
  background-color: #f5f5f5;
}

.option label {
  display: flex;
  align-items: center;
  cursor: pointer;
  width: 100%;
}

.option input {
  margin-right: 10px;
}
</style>