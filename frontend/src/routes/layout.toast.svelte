<script>
	import { fade } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import { toast } from '$lib/store.js';

	import SVG from '$lib/comp/svg.svelte';
	import Marked from '$lib/comp/marked.svelte';
	import Button from '$lib/button.svelte';

	const close = () => {
		$toast = '';
	};

	let zero = false;
	$: {
		zero = false;
		$toast;
		setTimeout(() => {
			zero = true;
		}, 0);

		setTimeout(() => {
			close();
		}, 5000);
	}
</script>

{#if $toast}
	<section
		class:good={$toast.status == 200}
		class:bad={$toast.status == 400}
		class:caution={$toast.status == 201}
		transition:fade={{ delay: 0, duration: 250, easing: cubicInOut }}
	>
		<div class="block">
			{#if $toast.status == 201}
				<SVG type="info" size="12" />
			{:else if $toast.status == 400}
				<SVG type="close" size="8" />
			{:else}
				<SVG type="check" size="12" />
			{/if}

			<Marked md={$toast?.message || 'no message'} />

			<Button icon="close" icon_size="10" class="tiny hover_red" on:click={close} />
		</div>

		<div class="progress" class:zero />
	</section>
{/if}

<style>
	section {
		width: fit-content;
		overflow: hidden;

		display: flex;
		flex-direction: column;
		align-items: end;

		border-radius: var(--sp0);
		color: var(--ac5_);
		font-size: small;
		fill: var(--ac5_);
	}

	.block {
		display: flex;
		align-items: center;
		gap: var(--sp2);

		padding: var(--sp2);
	}

	.progress {
		width: 100%;
		height: 2px;
		background-color: var(--ac5_);

		transition: width 5s linear;
	}
	.zero {
		width: 0;
	}

	.good {
		background-color: var(--cl5);
	}
	.bad {
		background-color: var(--cl4);
	}
	.caution {
		background-color: var(--cl6);
	}
</style>
