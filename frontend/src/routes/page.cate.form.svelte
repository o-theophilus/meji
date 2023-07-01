<script>
	import { goto } from '$app/navigation';
	import { module } from '$lib/store.js';
	import { state } from '$lib/page_state.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/comp/button.svelte';
	import SVG from '$lib/comp/svg2.svelte';
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Categories</div>
	</svelte:fragment>

	<div class="h">
		{#each $module.categories as category}
			<Button
				name={category.name}
				class="tiny"
				on:click={() => {
					$state['shop'].search = '';
					$state['shop'].category = category.name;
					$state['shop'].page_no = 1;
					$module = '';
					goto('/shop');
				}}
			>
				<SVG type={category.icon} size="20" />
			</Button>
		{/each}
	</div>
</Form>

<style>
	.h {
		justify-content: center;
	}
</style>
