<script>
	export let width = 0;
</script>

<div class="bar">
	<div class="fill" style:width="{width}%" />
</div>

<style>
	.bar {
		height: 20px;
		width: 100%;

		background-color: var(--ac5);
		border-radius: var(--sp0);

		overflow: hidden;
	}
	.fill {
		height: 100%;
		background-color: var(--cl6);
		width: 0;
	}
</style>
