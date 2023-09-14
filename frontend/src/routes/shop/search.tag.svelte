<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	export let tags = [];
	export let page_name = '';
	let show_tags = false;
	let search = '';
	let selected = [];
	let selected_snap = [];
	let logic = 'or';
	let logic_snap = 'or';

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('tag')) {
			let x = params.get('tag').split('$:');
			selected = x[0].split(',');
			logic = x[1];
		}
	});
</script>

<section>
	<button
		on:click={() => {
			show_tags = !show_tags;
			selected_snap = [...selected].sort((a, b) => a - b).join(',');
			logic_snap = `${logic}`;
		}}
	>
		Tags
		<!-- <SVG type="angle" /> -->
	</button>
	{#if show_tags}
		<div
			class="blocker"
			on:click|self={() => {
				show_tags = false;

				selected.sort((a, b) => a - b).join(',');
				if (selected != selected_snap || logic != logic_snap) {
					set_state(page_name, 'tag', `${selected}$:${logic}`);
				}
			}}
			role="presentation"
		/>
		<div class="drop">
			<div class="line">
				All Tags
				<div class="line">
					<input bind:group={logic} type="radio" value="and" />
					&
					<input bind:group={logic} type="radio" value="or" />
					or
				</div>
			</div>

			<br />
			<div class="input">
				<input bind:value={search} type="text" placeholder="Search" />
				{#if search}
					<div class="clear">
						<Button
							class="round small"
							on:click={() => {
								search = '';
							}}
						>
							<SVG type="close" />
						</Button>
					</div>
				{/if}
			</div>
			<br />
			<div class="tags">
				{#each tags as x}
					<div class="tag" class:hide={!x.includes(search)}>
						<input bind:group={selected} type="checkbox" value={x} />
						{x}
					</div>
				{/each}
			</div>
		</div>
	{/if}
</section>

<style>
	section {
		position: relative;
		z-index: 1;

		color: var(--ac2);
		fill: currentColor;
	}

	button {
		padding: var(--sp2) var(--sp4);
		background: none;
		border: none;
	}
	/* .category {
		width: min-content;
		background-color: var(--ac5);
		padding: var(--sp3);
		border-radius: var(--sp0);
	} */

	.blocker {
		position: fixed;
		inset: 0;
	}
	.drop {
		position: absolute;

		margin-top: var(--sp1);
		padding: var(--sp3);
		border-radius: var(--sp0);
		background-color: var(--ac5);
	}

	.line {
		display: flex;
		gap: var(--sp1);
		justify-content: space-between;
	}
	.input {
		position: relative;
	}

	input {
		padding-right: calc(var(--sp3) * 2);
		width: unset;
	}
	.clear {
		position: absolute;
		top: 0;
		right: var(--sp2);

		display: flex;
		align-items: center;
		height: 100%;
	}

	.tags {
		background-color: var(--ac5);

		max-height: 200px;
		overflow-y: auto;
	}
	.tag {
		display: flex;
		gap: var(--sp2);
		margin-top: var(--sp0);
	}
	.hide {
		display: none;
	}
</style>
