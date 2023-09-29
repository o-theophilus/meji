<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';
	import Center from '$lib/center.svelte';

	export let page_name;

	let search = '';
	let search_snap = '';

	const submit = () => {
		if (search_snap != search) {
			search_snap = `${search}`;
			set_state(page_name, 'search', search);
		}
	};

	onMount(async () => {
		let params = $page.url.searchParams;
		if (params.has('search')) {
			search = params.get('search');
		}
		search_snap = `${search}`;
	});
</script>

<Center>
	<section>
		<slot />

		<div class="input">
			<input
				class="search"
				class:show_close={search != ''}
				type="text"
				placeholder="Search for product"
				bind:value={search}
				on:keypress={(e) => {
					if (e.key == 'Enter') {
						submit();
					}
				}}
			/>

			<div class="btn">
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

				<Button disabled={search == search_snap} class="round small" on:click={submit}>
					<SVG type="search" size="15" />
				</Button>
			</div>
		</div>
	</section>
</Center>

<style>
	section {
		position: relative;

		display: flex;
		align-items: center;

		margin-top: var(--sp2);
		border: 2px solid var(--ac3);
		border-radius: var(--sp0);
		color: var(--ac3);
	}

	.input {
		position: relative;
		width: 100%;
	}

	input {
		border: none;
		padding: var(--sp2);
		padding-right: 48px;
		height: 100%;
	}
	.show_close {
		padding-right: 86px;
	}

	.btn {
		position: absolute;
		top: 0;
		right: var(--sp2);

		display: flex;
		align-items: center;
		gap: var(--sp1);

		height: 100%;
	}

	section:has(.search:hover),
	section:has(.search:focus) {
		border-color: var(--cl1);
	}
</style>
