<script>
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	export let placeholder = 'Search';
	export let search;
</script>

<div class="block">
	<div class="input">
		<div class="float svg">
			<SVG type="search" size="15" />
		</div>

		<input class:show_close={search != ''} type="text" {placeholder} bind:value={search} />

		<div class="float clear">
			{#if search}
				<Button
					class="small round"
					on:click={() => {
						search = '';
					}}
				>
					<SVG type="close" size="15" />
				</Button>
			{/if}
		</div>
	</div>

	<slot />
</div>

<style>
	.block {
		display: flex;
	}
	.input {
		position: relative;

		display: flex;
		align-items: center;

		width: 100%;

		fill: var(--ac3);
	}

	input {
		padding: var(--sp1);
		border-radius: var(--sp1);
		padding-left: var(--sp5);

		color: var(--ac1);
	}

	.show_close {
		padding-right: var(--sp5);
	}

	.float {
		position: absolute;
		top: 0;
		display: flex;
		align-items: center;
		height: 100%;
	}

	.clear {
		right: var(--sp2);
	}

	.svg {
		left: var(--sp2);
	}
</style>
