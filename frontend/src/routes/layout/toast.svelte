<script>
	import { fade } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import { toast } from '$lib/store.js';

	import SVG from '$lib/svg.svelte';
	import Marked from '$lib/marked.svelte';
	import BRound from '$lib/button/round.svelte';

	let timer_1, timer_2;
	const close = () => {
		$toast = '';
	};

	let zero = false;
	$: {
		$toast;

		zero = false;
		clearTimeout(timer_1);
		clearTimeout(timer_2);

		timer_1 = setTimeout(() => {
			zero = true;
		}, 0);
		timer_2 = setTimeout(close, 5000);
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
				<SVG icon="info" size="12" />
			{:else if $toast.status == 400}
				<SVG icon="close" size="8" />
			{:else}
				<SVG icon="check" size="12" />
			{/if}

			<Marked md={$toast?.message || 'no message'} />

			<BRound icon="close" icon_size="8" extra="hover_red" on:click={close} />
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
		color: var(--ac6_);
		font-size: small;
		fill: var(--ac6_);
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
		background-color: var(--ac6_);
	}
	.zero {
		transition: width 5s linear;
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
