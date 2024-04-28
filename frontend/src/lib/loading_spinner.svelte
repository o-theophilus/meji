<script>
	export let active = false;
	export let size = 50;
</script>

{#if active}
	<div class="circle" style:--size="{size}px" />
{/if}

<style>
	.circle {
		width: var(--size);
		height: var(--size);

		background-image: url('/image/loading.png');
		background-size: contain;
		background-repeat: no-repeat;

		animation: rotation 1s infinite linear;
	}

	@keyframes rotation {
		from {
			transform: rotate(0deg);
		}
		to {
			transform: rotate(359deg);
		}
	}
</style>
