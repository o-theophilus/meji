<script>
	import { goto } from '$app/navigation';
	import { module } from '$lib/store.js';
	import { state } from '$lib/page_state.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/comp/svg2.svelte';
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Tags</b>
	</svelte:fragment>

	<div class="tags">
		{#each $module.tags as tag}
			<Button
				name={tag}
				class="tiny"
				on:click={() => {
					// $state['shop'].search = '';
					// $state['shop'].tag = tag.name;
					// $state['shop'].page_no = 1;
					// $module = '';
					// goto('/shop');
				}}
			>
				<SVG type={tag} size="20" />
			</Button>
		{/each}
	</div>
</Form>

<style>
	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp1);
		/* justify-content: center; */
	}
</style>
