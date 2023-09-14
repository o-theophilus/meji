<script>
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	export let tags;
	export let selected;
	export let logic;
	let search = '';
</script>

<div class="blocker" on:click|self role="presentation" />
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

<style>
	.blocker {
		position: fixed;
		inset: 0;
	}
	.drop {
		position: absolute;
		top: 60px;
		left: 0;

		padding: var(--sp3);
		border-radius: var(--sp0);
		background-color: var(--ac5);
		color: var(--ac2);
		border: 1px solid var(--ac3);
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
