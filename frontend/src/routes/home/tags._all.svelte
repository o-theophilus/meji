<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { module, loading, state } from '$lib/store.js';

	import Form from '$lib/form.svelte';
	import Tag from '$lib/button.tag.svelte';
	import Input from '$lib/input.svelte';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	let tags = [];
	let filter = '';

	onMount(async () => {
		let i = $state.findIndex((x) => x.name == 'tags');
		if (i != -1) {
			tags = $state[i].data;
		}
	});
</script>

<Form>
	<svelte:fragment slot="title">
		<b>All Tags</b>
	</svelte:fragment>

	<div class="input">
		<Input bind:value={filter} type="text" placeholder="Filter" />
		{#if filter}
			<div class="clear">
				<Button
					class="round"
					on:click={() => {
						filter = '';
					}}
				>
					<SVG type="close" size="8" />
				</Button>
			</div>
		{/if}
	</div>

	<br />

	<div class="tags_space">
		{#each tags as tag}
			<Tag
				hide={!tag.includes(filter.toLowerCase())}
				on:click={() => {
					let i = $state.findIndex((x) => x.name == 'shop');
					if (i != -1) {
						$state[i].search = `?${new URLSearchParams({ tag }).toString()}`;
						$state[i].loaded = false;
					}

					$loading = 'loading . . .';
					$module = '';
					goto('/shop');
				}}
			>
				{tag}
			</Tag>
		{/each}
	</div>
</Form>

<style>
	.input {
		position: relative;
	}
	.clear {
		position: absolute;
		top: 0;
		right: var(--sp1);

		display: flex;
		align-items: center;
		height: 100%;
	}

	.tags_space {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp1);

		max-height: 200px;
		overflow-y: auto;

		border-radius: var(--sp1);
		padding: var(--sp1);
		border: 2px solid var(--ac4);
	}
</style>
